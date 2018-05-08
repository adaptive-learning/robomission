export function getToolbox(state, taskId) {
  const task = getTaskById(state, taskId);
  return getToolboxForTask(state, task);
}


// Note that task is a task record, not an ID, which is enforced by
// taskEnvironment requirments.
// TODO: Refactor so that this hack is not needed.
export function getToolboxForTask(state, task) {
  const toolboxId = getOption(task, state.problemSets, 'toolbox');
  if (toolboxId === null) {
    return [];
  }
  const toolbox = state.toolboxes[toolboxId].blocks;
  return toolbox;
}


export function getOption(task, problemSets, optionName) {
  if (optionName in task.setting) {
    return task.setting[optionName];
  }
  let problemSet = problemSets[task.problemSet];
  while (problemSet !== null && problemSet !== undefined) {
    if (optionName in problemSet.setting) {
      return problemSet.setting[optionName];
    }
    problemSet = problemSets[problemSet.parent];
  }
  return null;
}


export function getProblemSetId(state, taskId) {
  return state.tasks[taskId].problemSet;
}


export function getTaskById(state, taskId) {
  return state.tasks[taskId];
}


export function getTaskLevel(state, taskId) {
  const task = getTaskById(state, taskId);
  return task.level;
}
