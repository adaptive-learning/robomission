import { getPracticePageTaskId } from '../selectors/taskEnvironment';
import { getMode } from '../selectors/app';
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
  // Temporarily disabled.
  //const { level, activeCredits } = state.practice.shownLevelStatus;
  //const maxCredits = state.levels[level].credits;
  //const levelup = (activeCredits === maxCredits);
  //const hasNext = getNextLevelStatus(state) !== null;
  const level = 0;
  const activeCredits = 0;
  const maxCredits = 10;
  const levelup = false;
  const hasNext = false;
  return { level, activeCredits, maxCredits, levelup, hasNext };
}


export function getNextLevelStatus(state) {
  const current = state.practice.shownLevelStatus;
  const target = state.practice.targetLevelStatus;
  if (target === null) {
    return null;
  }
  const currentMaxCredits = state.levels[current.level].credits;
  if (current.level < target.level && current.activeCredits < currentMaxCredits) {
    // complete rest of the current level
    return {
      level: current.level,
      activeCredits: currentMaxCredits,
      maxCredits: currentMaxCredits,
      // levelup: true,
    };
  } else if (current.level + 1 < target.level) {
    // complete full next level
    return {
      level: current.level + 1,
      activeCredits: state.levels[current.level + 1].credits,
      maxCredits: state.levels[current.level + 1].credits,
      // levelup: true,
    };
  } else if (current.level < target.level ||
    (current.level === target.level && current.activeCredits < target.activeCredits)
  ) {
    // advance to target
    const targetMaxCredits = state.levels[target.level].credits;
    return {
      level: target.level,
      activeCredits: target.activeCredits,
      maxCredits: targetMaxCredits,
      // levelup: false,
    };
  }
  return null; // already at target
}


// maybe: get??AnimationTime(state)
//       animationTime: computeAnimationTime(
//         (target.activeCredits - current.activeCredits) / targetMaxCredits),
// animationTime: computeAnimationTime(1 - current.activeCredits / maxCredits),
//
// function computeAnimationTime(progressProportion) {
//   return 800 + progressBarProportion * 1400;
// }
