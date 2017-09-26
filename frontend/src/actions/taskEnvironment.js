import { CREATE_TASK_ENVIRONMENT,
         CLOSE_TASK_COMPLETION_DIALOG,
         SET_TASK,
         SET_TASK_SESSION,
         CHANGE_SETTING,
         CHANGE_CODE,
         CHANGE_ROBO_AST,
         RESET_GAME,
         DO_ACTION,
         MOVE,
         EVOLVE_WORLD,
         INTERPRETATION_STARTED,
         INTERPRETATION_FINISHED,
         CHANGE_GAME_PANEL_WIDTH,
         SET_EDITOR_TYPE } from '../action-types';
import { getTaskId,
         getTaskSessionId,
         getRoboAst,
         getCode,
         getLengthLimit,
         getEditorType,
         getTaskSourceText,
         isInterpreting } from '../selectors/taskEnvironment';
import { getColor, getPosition, isSolved, isDead, getGameStage } from '../selectors/gameState';
import { getToolbox } from '../selectors/task';
import { interpretRoboAst, interpretRoboCode, InterpreterError } from '../core/roboCodeInterpreter';
import { parseTaskSourceText } from '../core/taskSourceParser';
import { downloadTextFile, loadTextFile } from '../utils/files';
import { startTask, reportProgramExecution, reportProgramEdit } from '../actions/api';


export function createTaskEnvironment(taskEnvironmentId) {
  return {
    type: CREATE_TASK_ENVIRONMENT,
    payload: { taskEnvironmentId },
  };
}


export function startTaskInTaskEnvironment(taskEnvironmentId, taskId) {
  return (dispatch => {
    dispatch(setTaskById(taskEnvironmentId, taskId));
    // TODO: force sequential order to make sure task is started only after set
    // in task environment (to avoid potential taskSessionId resetting)
    return dispatch(startTask(taskId, taskEnvironmentId));
  });
}


export function setTaskSession(taskEnvironmentId, taskSession) {
  return {
    type: SET_TASK_SESSION,
    payload: { taskEnvironmentId, taskSession },
  };
}


// TODO: remove in favor of setTask[byId]
export function setTask(taskEnvironmentId, task) {
  return {
    type: SET_TASK,
    payload: { taskEnvironmentId, task },
  };
}


export function setTaskById(taskEnvironmentId, taskId) {
  // TODO: store only taskId in task environment to avoid redundant data in
  // store (requires nontrivial changes)
  return ((dispatch, getState) => {
    const state = getState();
    // inject toolbox needed for some reducers
    const task = {
      ...state.tasks[taskId],
      toolbox: getToolbox(state, taskId),
    };
    return dispatch(setTask(taskEnvironmentId, task));
  });
}


export function exportTask(taskEnvironmentId) {
  return (dispatch, getState) => {
    try {
      const taskId = getTaskId(getState(), taskEnvironmentId);
      const taskSourceText = getTaskSourceText(getState(), taskEnvironmentId);
      downloadTextFile(`${taskId}.md`, taskSourceText);
    } catch (err) {
      alert(`Export failed: ${err.message}`);
    }
  };
}


export function importTask(taskEnvironmentId) {
  return (dispatch) => {
    try {
      loadTextFile().then(taskSourceText => {
        const task = parseTaskSourceText(taskSourceText);
        dispatch(setTask(taskEnvironmentId, task));
      });
    } catch (err) {
      alert(`Import failed: ${err.message}`);
    }
  };
}


export function changeCode(taskEnvironmentId, code) {
  return {
    type: CHANGE_CODE,
    payload: { taskEnvironmentId, code },
  };
}


export function changeRoboAst(taskEnvironmentId, roboAst) {
  return (dispatch, getState) => {
    reportProgramEditInTaskEnvironment(dispatch, getState(), taskEnvironmentId, roboAst);
    return dispatch({
      type: CHANGE_ROBO_AST,
      payload: { taskEnvironmentId, roboAst },
    });
  };
}


export function changeSetting(taskEnvironmentId, taskSource) {
  return {
    type: CHANGE_SETTING,
    payload: { taskEnvironmentId, taskSource },
  };
}


function interpretationFinished(taskEnvironmentId) {
  return {
    type: INTERPRETATION_FINISHED,
    payload: { taskEnvironmentId },
  };
}


export function runProgram(taskEnvironmentId) {
  return (dispatch, getState) => {
    const actions = getLengthLimit(getState(), taskEnvironmentId);
    if (actions.limit !== null && actions.used > actions.limit) {
      const message = `Violated actions limit: ${actions.used}/${actions.limit}`;
      alert(message);
      return Promise.resolve(message);
    }
    const startingInterpretation = () => new Promise(resolve => {
      dispatch(interpretationStarted(taskEnvironmentId));
      setTimeout(resolve);
    });
    const context = {
      doActionMove: (action) => dispatch(doActionMove(taskEnvironmentId, action)),
      color: () => getColor(getState(), taskEnvironmentId),
      position: () => getPosition(getState(), taskEnvironmentId),
      isSolved: () => isSolved(getState(), taskEnvironmentId),
      isDead: () => isDead(getState(), taskEnvironmentId),
      interrupted: () => getGameStage(getState(), taskEnvironmentId) === 'initial',
    };
    const roboAst = getRoboAst(getState(), taskEnvironmentId);
    let interpret = () => interpretRoboAst(roboAst, context);
    const editorType = getEditorType(getState(), taskEnvironmentId);
    if (editorType === 'code') {
      const roboCode = getCode(getState(), taskEnvironmentId);
      interpret = () => interpretRoboCode(roboCode, context);
    }
    const interpretingPromise = startingInterpretation()
      .then(interpret)
      .catch(handleInterpreterError)
      .then(() => {
        dispatch(interpretationFinished(taskEnvironmentId));
        reportProgramExecutionInTaskEnvironment(dispatch, getState(), taskEnvironmentId);
      });
    return interpretingPromise;
  };
}


function reportProgramExecutionInTaskEnvironment(dispatch, state, taskEnvironmentId) {
  const taskSessionId = getTaskSessionId(state, taskEnvironmentId);
  if (taskSessionId == null) {
    return;
  }
  const ast = getRoboAst(state, taskEnvironmentId);
  const solved = isSolved(state, taskEnvironmentId);
  dispatch(reportProgramExecution(taskSessionId, ast, solved, taskEnvironmentId));
}


function reportProgramEditInTaskEnvironment(dispatch, state, taskEnvironmentId, newAst) {
  const taskSessionId = getTaskSessionId(state, taskEnvironmentId);
  if (taskSessionId == null) {
    return;
  }
  const oldAst = getRoboAst(state, taskEnvironmentId);
  dispatch(reportProgramEdit(taskSessionId, oldAst, newAst));
}


function handleInterpreterError(error) {
  if (error instanceof InterpreterError) {
    alert(error.message);
  } else {
    throw error;
  }
}


export function interpretationStarted(taskEnvironmentId) {
  return {
    type: INTERPRETATION_STARTED,
    payload: { taskEnvironmentId },
  };
}


export function doActionMove(taskEnvironmentId, action, interruptible = true) {
  return (dispatch, getState) => {
    const actionMovePromise = new Promise(resolve => {
      if (interruptible && !isInterpreting(getState(), taskEnvironmentId)) {
        resolve();
      } else {
        dispatch(doAction(taskEnvironmentId, action));
        setTimeout(resolve, 200);
      }
    }).then(() => {
      if (interruptible && !isInterpreting(getState(), taskEnvironmentId)) {
        return Promise.resolve('stopped');
      }
      dispatch(move(taskEnvironmentId));
      return new Promise(resolve => setTimeout(resolve, 200));
    }).then(() => {
      if (!interruptible || isInterpreting(getState(), taskEnvironmentId)) {
        dispatch(evolveWorld(taskEnvironmentId));
      }
    });
    return actionMovePromise;
  };
}


export function doAction(taskEnvironmentId, action) {
  return {
    type: DO_ACTION,
    payload: { taskEnvironmentId, action },
  };
}


export function move(taskEnvironmentId) {
  return {
    type: MOVE,
    payload: { taskEnvironmentId },
  };
}


export function evolveWorld(taskEnvironmentId) {
  return {
    type: EVOLVE_WORLD,
    payload: { taskEnvironmentId },
  };
}


export function resetGame(taskEnvironmentId) {
  return {
    type: RESET_GAME,
    payload: { taskEnvironmentId },
  };
}


export function changeGamePanelWidth(taskEnvironmentId, gamePanelWidth) {
  return {
    type: CHANGE_GAME_PANEL_WIDTH,
    payload: { taskEnvironmentId, gamePanelWidth },
  };
}


export function setEditorType(taskEnvironmentId, editorType) {
  return {
    type: SET_EDITOR_TYPE,
    payload: { taskEnvironmentId, editorType },
  };
}


export function closeTaskCompletionDialog(taskEnvironmentId) {
  return {
    type: CLOSE_TASK_COMPLETION_DIALOG,
    payload: { taskEnvironmentId },
  };
}
