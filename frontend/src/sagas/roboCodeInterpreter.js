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


function* stepJsCode(jsCode, effects) {
  let effect = null;
  let interpreterCallback = null;
  const createInterpreterApi = (interpreter, scope) => {
    const setFn = (name, getEffect) => {
      const fn = (...args) => {
        const callback = args.pop();
        effect = getEffect(...args);
        interpreterCallback = callback;
      };
      interpreter.setProperty(scope, name, interpreter.createAsyncFunction(fn));
    }
    const actionNames = ['fly', 'left', 'right', 'shoot'];
    for (const actionName of actionNames) {
      setFn(actionName, () => effects.doActionMove(actionName));
    }
    setFn('color', () => effects.color());
    setFn('position', () => effects.position());
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
    if (effect) {
      const interrupted = yield effects.interrupted();
      if (interrupted) {
        break;
      }
      const effectResult = yield effect;
      effect = null;
      const isSolved = yield effects.isSolved();
      if (isSolved) {
        break;
      }
      const isDead = yield effects.isDead();
      if (isDead) {
        break;
      }
      interpreterCallback(jsInterpreter.createPrimitive(effectResult));
    }
    // simple hack to avoid infinite loops:
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
