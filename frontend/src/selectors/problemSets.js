// Return ordered list of missions with their phases and their tasks.
// TODO: Rename to getProblemSetsNested().
export function getMissionList(state) {
  const psList = Object.values(state.problemSets);
  const missionList = psList.filter(ps => ps.granularity === 'mission');
  const orderedMissionList = missionList.sort((a, b) => a.level - b.level);
  const missionListInjected = orderedMissionList.map(mission => ({
    ...mission,
    phases: getPhaseList(state, mission),
  }));
  return missionListInjected;
}


function getPhaseList(state, mission) {
  return mission.parts.map(
    (psId, index) => getPhase(state, psId, index+1));
}


function getPhase(state, psId, index) {
  const phase = state.problemSets[psId];
  return ({
    ...phase,
    index,
    tasks: phase.tasks.map(taskId => state.tasks[taskId]),
  });
}


export function getToolboxId(state, psId) {
  return state.problemSets[psId].setting.toolbox;
}


// TODO: Remove if not needed.
//export function getProblemSetLevel(state, psId) {
//  return state.problemSets[psId].level;
//}
