import { getChunkLevel, getToolboxId } from '../selectors/chunk';


export function getChunkId(state, taskId) {
  // Faked becouse chunks are not set.
  // TODO: Use the following line once the task.chunk are available.
  //return state.tasks[taskId].chunk;
  return 'commands';  // fake
}


export function getTaskById(state, taskId) {
  return state.tasks[taskId];
}


export function getTaskLevel(state, taskId) {
  const chunkId = getChunkId(state, taskId);
  const level = getChunkLevel(state, chunkId);
  return level;
}


export function getToolbox(state, taskId) {
  // TODO: Generalize to work with the toolbox not specified in the immediate
  // parent.
  const chunkId = getChunkId(state, taskId);
  const toolboxId = getToolboxId(state, chunkId);
  const toolbox = state.toolboxes[toolboxId];
  return toolbox;
}
