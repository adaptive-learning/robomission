import { getPracticePageTaskId } from '../selectors/taskEnvironment';
import { getMode } from '../selectors/app';
import { getLevelStatus as getStudentLevelStatus } from '../selectors/student';
//import { getStudentLevel } from '../selectors/student';
//import { getTaskLevel } from '../selectors/task';


//function isTaskEasy(taskLevel, studentLevel) {
//  return taskLevel <= studentLevel / 2;
//}

export function getRecommendation(state) {
  const recommendation = { ...state.recommendation };
  // TODO: Remove notion of "easy recommendation".
  //const taskLevel = getTaskLevel(state, recommendation.task);
  //const studentLevel = getStudentLevel(state);
  //recommendation.isEasy = isTaskEasy(taskLevel, studentLevel);
  recommendation.isEasy = false;
  return recommendation;
}


export function getRecommendedTask(state) {
  const recommendation = getRecommendation(state);
  const { task, available } = recommendation;
  const taskId = task;  // TODO: make a single convention about naming id attributes
  if (!available) {
    return null;
  }
  if (getMode(state) === 'task' && getPracticePageTaskId(state) === taskId) {
    return null;
  }
  const url = `/task/${taskId}`;
  return { taskId, url };
}


export function getLevelStatus(state) {
  const levelStatus = {
    ...getStudentLevelStatus(state),
    levelup: false,
    hasNext: getNextLevelStatus(state) !== null
  };
  return levelStatus;
}


export function getNextLevelStatus(state) {
  if (!state.practice.progress) {
    return null;
  }
  const levelStatus = {
    ...getStudentLevelStatus(state),
    progress: state.practice.progress,
  }
  // TODO: extract state.practice.progress
  levelStatus.activeCredits = 90;
  return levelStatus;
}
