import * as at from '../action-types';


function action(type, payload = {}) {
  return {type, payload}
}


export const fetchApiRoot = {
  //request: () => action(at.FETCH_API_ROOT_REQUEST),
  success: (apiRoot) => action(at.FETCH_API_ROOT_SUCCESS, apiRoot),
  failure: (error) => action(at.FETCH_API_ROOT_FAILURE, {error}),
}


export const fetchWorld = {
  //request: () => action(at.FETCH_WORLD_REQUEST),
  success: (world) => action(at.FETCH_WORLD_SUCCESS, world),
  failure: (error) => action(at.FETCH_WORLD_FAILURE, {error}),
}


export const fetchUser = {
  request: (url) => action(at.FETCH_USER_REQUEST, {url}),
  success: (user) => action(at.FETCH_USER_SUCCESS, user),
  failure: (error) => action(at.FETCH_USER_FAILURE, {error}),
}


export const fetchStudent = {
  request: (url) => action(at.FETCH_STUDENT_REQUEST, {url}),
  success: (student) => action(at.FETCH_STUDENT_SUCCESS, student),
  failure: (error) => action(at.FETCH_STUDENT_FAILURE, {error}),
}


export const fetchPracticeOverview = {
  request: (url) => action(at.FETCH_PRACTICE_OVERVIEW_REQUEST, {url}),
  success: (practiceOverivew) => action(at.FETCH_PRACTICE_OVERVIEW_SUCCESS, practiceOverivew),
  failure: (error) => action(at.FETCH_PRACTICE_OVERVIEW_FAILURE, {error}),
}


export const startTask = {
  request: (taskEnvironmentId, taskId) => action(at.START_TASK_REQUEST, {taskEnvironmentId, taskId}),
  success: (taskSessionId) => action(at.START_TASK_SUCCESS, {taskSessionId}),
}


export const seeInstruction = {
  request: (instructionId) => action(at.SEE_INSTRUCTION_REQUEST, {instructionId}),
  success: (instructionId) => action(at.SEE_INSTRUCTION_SUCCESS, {instructionId}),
  failure: (error) => action(at.SEE_INSTRUCTION_FAILURE, {error}),
}


export const showLevelProgress = {
  start: () => action(at.SHOW_LEVEL_PROGRESS_START),
  next: (levelStatus) => action(at.SHOW_NEXT_LEVEL_STATUS, levelStatus),
}


export function createTaskEnvironment(taskEnvironmentId) {
  return action(at.CREATE_TASK_ENVIRONMENT, { taskEnvironmentId });
}


export function setTask(taskEnvironmentId, task) {
  return action(at.SET_TASK, { taskEnvironmentId, task });
}


export function setTaskById(taskEnvironmentId, taskId) {
  return action(at.SET_TASK_BY_ID, { taskEnvironmentId, taskId });
}


export function changeGamePanelWidth(taskEnvironmentId, gamePanelWidth) {
  return action(at.CHANGE_GAME_PANEL_WIDTH, { taskEnvironmentId, gamePanelWidth });
}


export function changeCode(taskEnvironmentId, code) {
  return action(at.CHANGE_CODE, { taskEnvironmentId, code });
}


export function changeRoboAst(taskEnvironmentId, roboAst) {
  return action(at.CHANGE_ROBO_AST, { taskEnvironmentId, roboAst });
}


export function runProgram(taskEnvironmentId) {
  return action(at.RUN_PROGRAM, { taskEnvironmentId });
}


export function interpretationStarted(taskEnvironmentId) {
  return action(at.INTERPRETATION_STARTED,  { taskEnvironmentId });
}


export function interpretationFinished(taskEnvironmentId) {
  return action(at.INTERPRETATION_FINISHED,  { taskEnvironmentId });
}


export function doActionMove(taskEnvironmentId, actionName, interruptible = true) {
  return action(at.DO_ACTION_MOVE, { taskEnvironmentId, action: actionName, interruptible });
}


export function doAction(taskEnvironmentId, actionName) {
  return action(at.DO_ACTION, { taskEnvironmentId, action: actionName });
}


export function move(taskEnvironmentId) {
  return action(at.MOVE, { taskEnvironmentId });
}


export function evolveWorld(taskEnvironmentId) {
  return action(at.EVOLVE_WORLD, { taskEnvironmentId });
}


export function resetGame(taskEnvironmentId) {
  return action(at.RESET_GAME, { taskEnvironmentId });
}


export function setOpenMenu(open) {
  return action(at.TOGGLE_MENU, { open });
}


export function changeLocation(newLocation) {
  return action(at.CHANGE_LOCATION, newLocation);
}


export function changeSetting(taskEnvironmentId, taskSource) {
  return action(at.CHANGE_SETTING, { taskEnvironmentId, taskSource });
}


export function setEditorType(taskEnvironmentId, editorType) {
  return action(at.SET_EDITOR_TYPE, { taskEnvironmentId, editorType });
}


export function switchVimMode() {
  return action(at.SWITCH_VIM_MODE);
}


export function exportTask(taskEnvironmentId) {
  return action(at.EXPORT_TASK, { taskEnvironmentId });
}


export function importTask(taskEnvironmentId) {
  return action(at.IMPORT_TASK, { taskEnvironmentId });
}


export function closeTaskCompletionDialog(taskEnvironmentId) {
  return action(at.CLOSE_TASK_COMPLETION_DIALOG, { taskEnvironmentId });
}


export function showInstructions() {
  return action(at.SHOW_INSTRUCTIONS);
}
