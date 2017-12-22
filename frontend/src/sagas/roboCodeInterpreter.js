// Saga for interpreting RoboCode
import { Interpreter } from 'js-interpreter';
import { getSyntaxCheckInfo } from '../core/roboCodeSyntaxChecker';
import { generateRoboJavaScript } from '../core/roboJavaScriptGenerator';


export function InterpreterError(message) {
  this.name = 'InterpreterError';
  this.message = message;
}


/**
 * Interpret given robo-ast step by step.
 *
 * @param {Object} roboAst - RoboCode AST as defined by core/roboCodeGrammar.
 * @param {Object} effects - IO effects yielded during interpretation.
 *                           (See interpretJsCode for their description.)
 * @yields IO effects such as actions and sensing.
 */
export function* interpretRoboAst(roboAst, effects) {
  const syntaxInfo = getSyntaxCheckInfo(roboAst);
  if (!syntaxInfo.valid) {
    const report = syntaxInfo.errors[0].message;
    throw new InterpreterError(report);
  }
  const jsCode = generateRoboJavaScript(roboAst);
  yield* stepJsCode(jsCode, effects);
}


/**
 * Interpret given JavaScript step by step.
 *
 * @param {String} jsCode - JavaScript code to interpret.
 * @param {Object} effects - IO effects yielded during interpretation.
 *    effects.isStopped() -> Is execution interrupted/finished?
 *    effects.sense(sensor) -> What is the value of given sensor (e.g. color)?
 *    effects.doAction(action) -> Perform given action (e.g. fly, shoot).
 *    effects.highlightBlock(blockId) -> Highlight given block.
 *
 * @yields IO effects such as actions and sensing.
 */
function* stepJsCode(jsCode, effects) {
  // In order to enable yielding IO effects, we set up "coroutines-like"
  // communication between the top-level generator and the low-level interpreter.
  // (IO effects cannot be yielded directly from non-generator functions, i.e.
  // it's not possible to use yield in functions passed to the js-interpeter.)
  // When an interpreter encounters an IO function, it sets the following
  // variable to mark what effect it wants to perform:
  let effectToYield = null;
  // And sets a callback function to call after the effect is resolved:
  let interpreterCallback = null;
  // Js-Interpreter requires API as a function that takes an instance of an
  // interpreter and scope and sets the API calls via interpreter.setProperty.
  // (Details: https://neil.fraser.name/software/JS-Interpreter/docs.html)
  const createInterpreterApi = (interpreter, scope) => {
    // Helper function to define a new API function under given `name`.
    // It sets the `effectToYield` and blocks the execution until
    // `interpreterCallback` is called after the effect is resolved.
    const setFn = (name, getEffect) => {
      const fn = (...args) => {
        const callback = args.pop();
        effectToYield = getEffect(...args);
        interpreterCallback = callback;
      };
      interpreter.setProperty(scope, name, interpreter.createAsyncFunction(fn));
    }
    // Define API calls for acting, sensing, and block highlighting.
    const actionNames = ['fly', 'left', 'right', 'shoot'];
    for (const actionName of actionNames) {
      setFn(actionName, () => effects.doAction(actionName));
    }
    const sensorNames = ['color', 'position'];
    for (const sensorName of sensorNames) {
      setFn(sensorName, () => effects.sense(sensorName));
    }
    setFn('highlightBlock', (blockId) => effects.highlightBlock(blockId.toString()));
  }
  const jsInterpreter = new Interpreter(jsCode, createInterpreterApi);
  let next = true;
  let step = 0;
  while (next) {
    try {
      next = jsInterpreter.step();
    } catch (error) {
      handleInterpreterError(error);
    }
    step += 1;
    if (effectToYield) {
      const stopped = yield effects.isStopped();
      if (stopped) {
        break;
      }
      const effectResult = yield effectToYield;
      effectToYield = null;
      interpreterCallback(jsInterpreter.createPrimitive(effectResult));
    }
    // Simple hack to avoid infinite loops:
    if (step > 10000) {
      throw new InterpreterError('Maximum step reached. Probably an infinite loop.');
    }
  }
}


function handleInterpreterError(error) {
  if (error instanceof ReferenceError) {
    let suggestion = '';
    if (error.message.startsWith('move is not defined')) {
      suggestion = ' (Did you mean "fly"?)';
    }
    const report = `InterpreterError: ${error.message}${suggestion}`;
    throw new InterpreterError(report);
  } else {
    throw error;
  }
}
