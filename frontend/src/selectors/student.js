export function getLevelStatus(state) {
  const level = state.student.level;
  const activeCredits = state.student.activeCredits;
  // current level specify number of credits the student needs to level up
  const maxCredits = state.levels[level].credits;
  return { level, activeCredits, maxCredits };
}


export function isNewStudent(state) {
  return state.student.credits === 0;
}
