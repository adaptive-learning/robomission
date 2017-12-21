import { CHANGE_LOCATION,
         CREATE_TASK_ENVIRONMENT,
         CLOSE_TASK_COMPLETION_DIALOG,
         SET_TASK,
         START_TASK_SUCCESS,
         CHANGE_SETTING,
         EDIT_PROGRAM_CODE,
         EDIT_PROGRAM_AST,
         RESET_GAME,
         DO_ACTION,
         MOVE,
         EVOLVE_WORLD,
         HIGHLIGHT_BLOCK,
         INTERPRETATION_STARTED,
         INTERPRETATION_FINISHED,
         CHANGE_GAME_PANEL_WIDTH,
         SET_EDITOR_TYPE,
         SET_SPEED,
         RUN_PROGRAM_SOLVED_REPORT } from '../action-types';
import { parseSpaceWorld } from '../core/spaceWorldDescription';
import { parseRoboCode, RoboCodeSyntaxError } from '../core/roboCodeParser';
import { generateRoboCode } from '../core/roboCodeGenerator';
import { practicePageTaskEnvironmentId } from '../selectors/taskEnvironment';


export default function reduceTaskEnvironments(state = {}, action) {
  switch (action.type) {
    case CREATE_TASK_ENVIRONMENT:
      return createTaskEnvironment(state, action.payload.taskEnvironmentId);
    case CLOSE_TASK_COMPLETION_DIALOG:
      return updateTaskEnvironment(state, closeTaskCompletionDialog, action.payload);
    case CHANGE_LOCATION:
      // make sure that task completion modal is closed when leave the practice
      // page e.g. by clicking on "tasks overview" button
      return updateTaskEnvironment(state, closeTaskCompletionDialog,
        { taskEnvironmentId: practicePageTaskEnvironmentId });
    case START_TASK_SUCCESS:
      return updateTaskEnvironment(state, setTaskSessionId, action.payload);
    case SET_TASK:
      return updateTaskEnvironment(state, setTask, action.payload);
   case CHANGE_SETTING:
      return updateTaskEnvironment(state, changeSetting, action.payload);
    case DO_ACTION:
      return updateTaskEnvironment(state, doAction, action.payload);
    case MOVE:
      return updateTaskEnvironment(state, move, action.payload);
    case EVOLVE_WORLD:
      return updateTaskEnvironment(state, evolveWorld, action.payload);
    case HIGHLIGHT_BLOCK:
      return updateTaskEnvironment(state, highlightBlock, action.payload);
    case RESET_GAME:
      return updateTaskEnvironment(state, resetGame, action.payload);
    case SET_SPEED:
      return updateTaskEnvironment(state, setSpeed, action.payload);
    case EDIT_PROGRAM_CODE:
      return updateTaskEnvironment(state, changeCode, action.payload);
    case EDIT_PROGRAM_AST:
      return updateTaskEnvironment(state, changeRoboAst, action.payload);
    case INTERPRETATION_STARTED:
      return updateTaskEnvironment(state, startInterpretation, action.payload);
    case INTERPRETATION_FINISHED:
      return updateTaskEnvironment(state, endInterpretation, action.payload);
    case CHANGE_GAME_PANEL_WIDTH:
      return updateTaskEnvironment(state, changeGamePanelWidth, action.payload);
    case SET_EDITOR_TYPE:
      return updateTaskEnvironment(state, setEditorType, action.payload);
    case RUN_PROGRAM_SOLVED_REPORT:
      return updateTaskEnvironment(state, solveTask, action.payload);
    default:
      return state;
  }
}


// TODO: freeze?
const emptyTask = {
  id: '',
  setting: {
    fields: [[]],
    length: null,
    energy: null,
  },
};


// TODO: freeze?
// export const initialTaskEnvironment = {
const initialTaskEnvironment = {
  task: emptyTask,
  taskSessionId: null,
  editorType: 'blockly',
  editorSessionId: 0,
  roboAst: { head: 'start', body: [] },
  code: '',
  validCode: true,
  interpreting: false,
  pastActions: [],
  currentAction: null,
  gamePanelWidth: 280,
  isTaskCompletionDialogOpen: false,
  highlightedBlock: null,
  speed: 3,
};


function createTaskEnvironment(taskEnvironments, taskEnvironmentId) {
  if (taskEnvironmentId in taskEnvironments) {
    return taskEnvironments;
  }
  return { ...taskEnvironments, [taskEnvironmentId]: initialTaskEnvironment };
}


function updateTaskEnvironment(taskEnvironments, updateFn, args) {
  return updateEntity(taskEnvironments, args.taskEnvironmentId, updateFn, args);
}


function updateEntity(entities, id, updateFn, args) {
  const oldEntity = (id in entities) ? entities[id] : initialTaskEnvironment;
  const updatedEntity = updateFn(oldEntity, args);
  return { ...entities, [id]: updatedEntity };
}


function setTaskSessionId(taskEnvironment, { taskSessionId }) {
  return {
    ...taskEnvironment,
    taskSessionId,
  };
}


function setTask(taskEnvironment, { task }) {
  const taskWithDefaults = addDefaults(task);
  return {
    ...taskEnvironment,
    taskSessionId: null,
    editorSessionId: taskEnvironment.editorSessionId + 1,
    task: taskWithDefaults,
    roboAst: { head: 'start', body: [] },
    code: '',
    validCode: true,
    pastActions: [],
    currentAction: null,
    interpreting: false,
    isTaskCompletionDialogOpen: false,
    highlightedBlock: null,
  };
}


function addDefaults(task) {
  // TODO: better way to specify defaults?
  const setting = {
    length: null,
    energy: null,
    ...task.setting,
  };
  const taskWithDefaults = {
    categoryId: null,
    ...task,
    setting,
  };
  return taskWithDefaults;
}


function changeSetting(taskEnvironment, { taskSource }) {
  const { task, invalidSpaceWorldText } = taskEnvironment;
  const { id, category, energy, length, spaceWorldText } = taskSource;
  let newInvalidSpaceWorldText = invalidSpaceWorldText;
  let newFields = null;
  if (spaceWorldText !== undefined) {
    try {
      newFields = parseSpaceWorld(spaceWorldText);
      newInvalidSpaceWorldText = null;
    } catch (err) {
      newFields = null;
      newInvalidSpaceWorldText = spaceWorldText;
    }
  }
  const updatedTask = {
    id: (id !== undefined) ? id : task.id,
    category: (category !== undefined) ? category : task.category,
    setting: {
      fields: (newFields !== null) ? newFields : task.setting.fields,
      energy: (energy !== undefined) ? energy : task.setting.energy,
      length: (length !== undefined) ? length : task.setting.length,
    },
  };
  const updatedTaskWithDefaults = addDefaults(updatedTask);
  const updatedTaskEnvironment = {
    ...taskEnvironment,
    task: updatedTaskWithDefaults,
    invalidSpaceWorldText: newInvalidSpaceWorldText,
  };
  return updatedTaskEnvironment;
}


function changeCode(taskEnvironment, { code }) {
  let roboAst = taskEnvironment.roboAst;
  let validCode = true;
  try {
    roboAst = parseRoboCode(code);
  } catch (error) {
    if (error instanceof RoboCodeSyntaxError) {
      validCode = false;
    } else {
      throw error;
    }
  }
  return { ...taskEnvironment, code, validCode, roboAst };
}


function changeRoboAst(taskEnvironment, { roboAst }) {
  const code = generateRoboCode(roboAst);
  const validCode = true;
  return { ...taskEnvironment, code, validCode, roboAst };
}


function doAction(taskEnvironment, { action }) {
  const updatedTaskEnvironment = { ...taskEnvironment, currentAction: action };
  return updatedTaskEnvironment;
}


function move(taskEnvironment) {
  const { pastActions, currentAction } = taskEnvironment;
  const augmentedPastActions = (currentAction) ? [...pastActions, currentAction] : pastActions;
  const updatedTaskEnvironment = {
    ...taskEnvironment,
    pastActions: augmentedPastActions,
    currentAction: null,
  };
  return updatedTaskEnvironment;
}


function evolveWorld(taskEnvironment) {
  const updatedTaskEnvironment = {
    ...taskEnvironment,
    pastActions: [...taskEnvironment.pastActions, 'world-evolution'],
  };
  return updatedTaskEnvironment;
}


function highlightBlock(taskEnvironment, { blockId }) {
  const updatedTaskEnvironment = {
    ...taskEnvironment,
    highlightedBlock: blockId,
  };
  return updatedTaskEnvironment;
}


function resetGame(taskEnvironment) {
  return {
    ...taskEnvironment,
    interpreting: false,
    pastActions: [],
    currentAction: null,
  };
}


function setSpeed(taskEnvironment, { speed }) {
  return {
    ...taskEnvironment,
    speed,
  };
}


function startInterpretation(taskEnvironment) {
  return { ...taskEnvironment, interpreting: true };
}


function endInterpretation(taskEnvironment) {
  return { ...taskEnvironment, interpreting: false, highlightedBlock: null };
}


function changeGamePanelWidth(taskEnvironment, { gamePanelWidth }) {
  return { ...taskEnvironment, gamePanelWidth };
}


function setEditorType(taskEnvironment, { editorType }) {
  return { ...taskEnvironment, editorType };
}


function solveTask(taskEnvironment) {
  return { ...taskEnvironment, isTaskCompletionDialogOpen: true };
}


function closeTaskCompletionDialog(taskEnvironment) {
  return { ...taskEnvironment, isTaskCompletionDialogOpen: false };
}

export { initialTaskEnvironment };
