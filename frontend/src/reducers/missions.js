import { FETCH_WORLD_SUCCESS } from '../action-types';

export default function reduceMissions(state = {}, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
      const missionList = action.payload.missions.map(parseMission);
      const missions = {};
      for (const mission of missionList) {
        missions[mission.id] = mission;
      }
      return missions;
    }
    default: {
      return state;
    }
  }
}

function parseMission(data) {
  const mission = {
    id: data['name'],
    order: data['order'],
    chunk: data['chunk'],
  };
  return mission;
}
