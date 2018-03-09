// Return ordered list of missions with their phases and their tasks.
export function getMissionList(state) {
  const { missions } = state;
  const allMissionIds = Object.keys(missions);
  const compareMissionIds = (a, b) => (missions[a].order - missions[b].order);
  const orderedMissionIds = allMissionIds.sort(compareMissionIds);
  const missionList = orderedMissionIds.map(missionId => ({
    ...missions[missionId],
    phases: getPhaseList(state, missionId),
  }));
  // TODO: Inject phases and missions.
  return missionList;
}


function getPhaseList(state, missionId) {
  const parentChunk = state.chunks[state.missions[missionId].chunk];
  return parentChunk.subchunks.map(
    (chunkId, index) => getPhase(state, chunkId, index+1));
}


function getPhase(state, chunkId, index) {
  const phase = state.chunks[chunkId];
  return ({
    ...phase,
    index,
    tasks: phase.tasks.map(taskId => state.tasks[taskId]),
  });
}
