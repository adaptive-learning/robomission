export function getLevelStatus(state) {
  const level = state.student.level;
  // TODO: Remove notion of activeCredits; replace progressbar by stepper.
  // Temporarily activeCredits are set to correspond to the mastered skill
  // (percentage).
  const currentChunkId = state.missions[state.student.mission].chunk;
  const skill = state.chunks[currentChunkId].skill;
  const activeCredits = Math.floor(100 * skill);
  const maxCredits = 100;
  return { level, activeCredits, maxCredits };
}


export function getStudentLevel(state) {
  return state.student.level;
}


export function isNewStudent(state) {
  return state.student.credits === 0;
}


export function getStudentUrl(state) {
  return state.user.studentUrl;
}


export function getPracticeOverviewUrl(state) {
  return state.student.practiceOverviewUrl;
}


export function getStartTaskUrl(state) {
  return state.student.startTaskUrl;
}


export function getReportProgramExecutionUrl(state) {
  return state.student.reportProgramExecutionUrl;
}


export function getReportProgramEditUrl(state) {
  return state.student.reportProgramEditUrl;
}


export function getWatchInstructionUrl(state) {
  return state.student.watchInstructionUrl;
}
