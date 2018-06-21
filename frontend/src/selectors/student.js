export function getLevelStatus(state) {
  const level = state.student.level;
  // TODO: Remove notion of activeCredits; replace progressbar by stepper.
  // Temporarily activeCredits are set to correspond to the mastered skill
  // (percentage).
  let activeCredits = 100
  const maxCredits = 100;
  if (state.student.mission !== null) {
    const currentProblemSet = state.problemSets[state.student.mission];
    const skill = currentProblemSet.skill;
    activeCredits = (skill !== undefined) ? Math.floor(100 * skill) : 0;
  }
  const missionCompleted = activeCredits >= maxCredits;
  const nextMissionId = missionCompleted ? state.recommendation.mission : null;
  return { level, missionCompleted, nextMissionId, activeCredits, maxCredits };
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
