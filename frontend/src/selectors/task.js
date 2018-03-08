import { getChunkLevel, getToolboxId } from '../selectors/chunk';


export function getToolbox(state, taskId) {
  const task = getTaskById(state, taskId);
  return getToolboxForTask(state, task);
}


// Note that task is a a task record, not an ID, which is enforced by
// taskEnvironment requirments.
// TODO: Refactor so that this hack is not needed.
export function getToolboxForTask(state, task) {
  const toolboxId = getOption(task, state.chunks, 'toolbox');
  if (toolboxId === null) {
    return [];
  }
  const toolbox = state.toolboxes[toolboxId].blocks;
  return toolbox;
}


function getOption(task, chunks, optionName) {
  if (optionName in task.setting) {
    return task.setting[optionName];
  }
  let chunk = chunks[task.chunk];
  while (chunk !== null && chunk !== undefined) {
    if (optionName in chunk.setting) {
      return chunk.setting[optionName];
    }
    chunk = chunks[chunk.parentChunk];
  }
  return null;
}


export function getChunkId(state, taskId) {
  return state.tasks[taskId].chunk;
}


export function getTaskById(state, taskId) {
  return state.tasks[taskId];
}


export function getTaskLevel(state, taskId) {
  const chunkId = getChunkId(state, taskId);
  const level = getChunkLevel(state, chunkId);
  return level;
}
