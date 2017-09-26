import { Interpreter } from 'js-interpreter';
import { parseRoboCode, RoboCodeSyntaxError } from './roboCodeParser';
import { getSyntaxCheckInfo } from './roboCodeSyntaxChecker';
import { generateRoboJavaScript } from './roboJavaScriptGenerator';

const defaultSettings = {
  pauseLength: 600,
};


/**
 * Interpret given robo-ast step by step.
 *
 * Input and output is given by :context: parameter, it must provide
 * all robo-commands (doActionMove, position, color)
 * and it can optionally provide some other hooks (isSolved, isDead, interrupted).
 *
 * Return a promise which will be fullfilled when the interpretting is finished
 */
export function interpretRoboAst(roboAst, context, settings = defaultSettings) {
  const syntaxInfo = getSyntaxCheckInfo(roboAst);
  if (!syntaxInfo.valid) {
    const report = syntaxInfo.errors[0].message;
    return Promise.reject(new InterpreterError(report));
  }
  const jsCode = generateRoboJavaScript(roboAst);
  const interpretingFinishedPromise = steppingJsCode(jsCode, context, settings.pauseLength);
  return interpretingFinishedPromise;
}


export function interpretRoboCode(code, context, settings = defaultSettings) {
  let roboAst = null;
  try {
    roboAst = parseRoboCode(code);
  } catch (error) {
    if (error instanceof RoboCodeSyntaxError) {
      return Promise.reject(new InterpreterError(error.message));
    }
    throw error;
  }
  return interpretRoboAst(roboAst, context, settings);
}


export function InterpreterError(message) {
  this.name = 'InterpreterError';
  this.message = message;
}


function steppingJsCode(jsCode, context, pauseLength) {
  let pause = false;

  function initApi(interpreter, scope) {
    // TODO: dry initApi function
    const actions = ['fly', 'left', 'right', 'shoot'];
    actions.forEach((action) => {
      interpreter.setProperty(scope, action,
        interpreter.createNativeFunction(() => {
          context.doActionMove(action);
          pause = true;
          return interpreter.createPrimitive();
        })
      );
    });

    interpreter.setProperty(scope, 'color',
      interpreter.createNativeFunction(() => interpreter.createPrimitive(context.color()))
    );

    interpreter.setProperty(scope, 'position',
      interpreter.createNativeFunction(() => interpreter.createPrimitive(context.position()))
    );
  }

  const jsInterpreter = new Interpreter(jsCode, initApi);

  function nextSteps(resolve, reject) {
    if (context.interrupted()) {
      resolve('interrupted');
    } else if (context.isSolved()) {
      finalize(resolve, 'solved');
    } else if (context.isDead()) {
      finalize(resolve, 'dead');
    } else {
      let next = true;
      while (next && !pause) {
        try {
          next = jsInterpreter.step();
        } catch (error) {
          if (error instanceof ReferenceError) {
            let suggestion = '';
            if (error.message.startsWith('move is not defined')) {
              suggestion = ' (Did you mean "fly"?)';
            }
            const report = `InterpreterError: ${error.message}${suggestion}`;
            reject(new InterpreterError(report));
            return;
          }
          throw error;
        }
      }
      if (!next) {
        finalize(resolve, 'last step');
      } else {
        pause = false;
        setTimeout(() => nextSteps(resolve, reject), pauseLength);
      }
    }
  }

  function finalize(resolve, reason) {
    setTimeout(() => {
      // context.finalize();
      resolve(reason);
    }, pauseLength);
  }

  return new Promise(nextSteps);
}
