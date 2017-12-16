import { getCategoryLevel, getToolboxId } from '../selectors/category';


export function getCategoryId(state, taskId) {
  return state.tasks[taskId].category;
}


export function getTaskById(state, taskId) {
  return state.tasks[taskId];
}


export function getTaskLevel(state, taskId) {
  const categoryId = getCategoryId(state, taskId);
  const level = getCategoryLevel(state, categoryId);
  return level;
}


export function getToolbox(state, taskId) {
  const categoryId = getCategoryId(state, taskId);
  const toolboxId = getToolboxId(state, categoryId);
  const toolbox = state.toolboxes[toolboxId];
  return toolbox;
}
