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

  function initApi(interpreter, scope) {
    // TODO: dry initApi function
    const actions = ['fly', 'left', 'right', 'shoot'];
    actions.forEach((action) => {
      interpreter.setProperty(scope, action,
        interpreter.createAsyncFunction((callback) => {
          effect = effects.doActionMove(action);
          interpreterCallback = callback;
        })
      );
    });

    interpreter.setProperty(scope, 'color',
      interpreter.createAsyncFunction((callback) => {
        effect = effects.color();
        interpreterCallback = callback;
      })
    );

    interpreter.setProperty(scope, 'position',
      interpreter.createAsyncFunction((callback) => {
        effect = effects.position();
        interpreterCallback = callback;
      })
    );

    interpreter.setProperty(scope, 'highlightBlock',
      interpreter.createAsyncFunction((blockIdValue, callback) => {
        const blockId = blockIdValue.toString();
        effect = effects.highlightBlock(blockId);
        interpreterCallback = callback;
      })
    );
  }

  const jsInterpreter = new Interpreter(jsCode, initApi);
  let next = true;
  let step = 0;
  while (next) {
    try {
      next = jsInterpreter.step();
    } catch (error) {
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
