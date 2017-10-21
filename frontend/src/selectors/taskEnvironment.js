import { countStatements } from '../core/roboCodeSyntaxChecker';
import { generateSpaceWorldText } from '../core/spaceWorldDescription';
import { stripIndentation } from '../utils/text';
import { initialTaskEnvironment } from '../reducers/taskEnvironments';
import { getToolboxId } from '../selectors/category';

export const practicePageTaskEnvironmentId = 'practice-page';

export function getTaskEnvironment(state, taskEnvironmentId) {
  const taskEnvironment = state.taskEnvironments[taskEnvironmentId];
  if (taskEnvironment === undefined) {
    return initialTaskEnvironment;
  }
  return taskEnvironment;
}


export function getTask(state, taskEnvironmentId) {
  return getTaskEnvironment(state, taskEnvironmentId).task;
}


export function getTaskSessionId(state, taskEnvironmentId) {
  return getTaskEnvironment(state, taskEnvironmentId).taskSessionId;
}


export function getPracticePageTaskId(state) {
  return getTaskId(state, practicePageTaskEnvironmentId);
}


export function getTaskId(state, taskEnvironmentId) {
  const task = getTask(state, taskEnvironmentId);
  return task.id;
}


export function getToolbox(state, taskEnvironmentId) {
  // using task version stored in the environment to make it work in task
  // editor as well
  const task = getTask(state, taskEnvironmentId);
  if (task === undefined || task.category === undefined) {
    return [];
  }
  const categoryId = task.category;
  const toolboxId = getToolboxId(state, categoryId);
  const toolbox = state.toolboxes[toolboxId];
  return toolbox.blocks;
}

export function getEditorSessionId(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.editorSessionId;
}


export function getLengthLimit(state, taskEnvironmentId) {
  const task = getTask(state, taskEnvironmentId);
  const limit = task.setting.length;
  const roboAst = getRoboAst(state, taskEnvironmentId);
  const used = countStatements(roboAst);
  return { used, limit };
}


export function getTaskSourceText(state, taskEnvironmentId) {
  if (!isSpaceWorldTextValid(state, taskEnvironmentId)) {
    throw Error('Invalid task setting');
  }
  const { id, category, setting } = getTask(state, taskEnvironmentId);
  const { energy, length } = setting;
  const spaceWorldText = getSpaceWorldText(state, taskEnvironmentId);
  const solution = getCode(state, taskEnvironmentId);

  const sourceText = stripIndentation`\
    # ${id}
    ${category !== null ? `- category: ${category}` : ''}

    ## Setting

    \`\`\`
    ${spaceWorldText}
    \`\`\`
    ${energy !== null ? `- energy: ${energy}` : ''}
    ${length !== null ? `- length: ${length}` : ''}

    ## Solution

    \`\`\`
    ${solution}
    \`\`\`
  `;
  return sourceText;
}


export function getSetting(state, taskEnvironmentId) {
  const task = getTask(state, taskEnvironmentId);
  return task.setting;
}


export function getSpaceWorldText(state, taskEnvironmentId) {
  if (!isSpaceWorldTextValid(state, taskEnvironmentId)) {
    const invalidSpaceWorldText = getInvalidSpaceWorldText(state, taskEnvironmentId);
    return invalidSpaceWorldText;
  }
  const setting = getSetting(state, taskEnvironmentId);
  const spaceWorldText = generateSpaceWorldText(setting.fields);
  return spaceWorldText;
}


export function getInvalidSpaceWorldText(state, taskEnvironmentId) {
  const { invalidSpaceWorldText } = getTaskEnvironment(state, taskEnvironmentId);
  if (invalidSpaceWorldText === undefined) {
    return null;
  }
  return invalidSpaceWorldText;
}


export function isSpaceWorldTextValid(state, taskEnvironmentId) {
  const { invalidSpaceWorldText } = getTaskEnvironment(state, taskEnvironmentId);
  const isValid = (invalidSpaceWorldText == null);
  return isValid;
}


export function getCode(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.code;
}


export function getRoboAst(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.roboAst;
}


export function getEditorType(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  const editorType = taskEnvironment.editorType;
  return editorType;
}


export function getGamePanelWidth(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.gamePanelWidth;
}


export function isInterpreting(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.interpreting;
}


export function isTaskCompletionDialogOpen(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.isTaskCompletionDialogOpen;
}


// FIXME: not a selector function, should be somewhere else
export function getInitialFieldsFromTaskEnvironment(taskEnvironment) {
  return taskEnvironment.task.setting.fields;
}
