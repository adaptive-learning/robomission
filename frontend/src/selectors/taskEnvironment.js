import { countStatements } from '../core/roboCodeSyntaxChecker';
import { generateSpaceWorldText } from '../core/spaceWorldDescription';
import { generateMiniRoboCode } from '../core/miniRoboCodeGenerator';
import { stripIndentation } from '../utils/text';
import { initialTaskEnvironment } from '../reducers/taskEnvironments';
import { getToolboxForTask, getOption } from '../selectors/task';

export const practicePageTaskEnvironmentId = 'practice-page';

export function getTaskEnvironment(state, taskEnvironmentId) {
  const taskEnvironment = state.taskEnvironments[taskEnvironmentId];
  if (taskEnvironment === undefined) {
    return initialTaskEnvironment;
  }
  return taskEnvironment;
}


export function getTask(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  // TODO: Merge all parent chunks setting into the task setting.
  return {
    ...taskEnvironment.task,
    setting: {
      ...taskEnvironment.task.setting,
      toolbox: getOption(taskEnvironment.task, state.chunks, 'toolbox'),
    },
  };
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


export function getTaskLevel(state, taskEnvironmentId) {
  const task = getTask(state, taskEnvironmentId);
  const categoryId = task.category;
  if (!categoryId) {
    return 0;
  }
  const category = state.categories[categoryId];
  const level = category.level;
  return level;
}


export function getToolbox(state, taskEnvironmentId) {
  // Using task version stored in the environment to make it work in task
  // editor as well.
  const task = getTask(state, taskEnvironmentId);
  if (task === undefined) {
    return [];
  }
  return getToolboxForTask(state, task);
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
  const { id, setting } = getTask(state, taskEnvironmentId);
  const { toolbox, energy, length } = setting;
  const spaceWorldText = getSpaceWorldText(state, taskEnvironmentId);
  const solution = getCode(state, taskEnvironmentId);

  const sourceText = stripIndentation`\
    # ${id}

    ## Setting

    \`\`\`
    ${spaceWorldText}
    \`\`\`
    ${toolbox !== null ? `- toolbox: ${toolbox}` : ''}
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


export function getMiniRoboCode(state, taskEnvironmentId) {
  const roboAst = getRoboAst(state, taskEnvironmentId)
  const miniRoboCode = generateMiniRoboCode(roboAst);
  return miniRoboCode;
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


export function getHighlightedBlock(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.highlightedBlock;
}


export function getSpeed(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  return taskEnvironment.speed;
}


export function getPauseLength(state, taskEnvironmentId) {
  const speed = getSpeed(state, taskEnvironmentId);
  const speedToPause = {
    1: 1400,
    2: 800,
    3: 400,
    4: 100,
    5: 0,
  };
  const pause = speedToPause[speed];
  return pause;
}


// FIXME: not a selector function, should be somewhere else
export function getInitialFieldsFromTaskEnvironment(taskEnvironment) {
  return taskEnvironment.task.setting.fields;
}
