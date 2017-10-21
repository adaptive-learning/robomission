import { FETCH_WORLD_SUCCESS } from '../action-types';

export default function reduceLevels(state = {}, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
      const levelList = action.payload.levels.map(parseLevel);
      const levels = {};
      for (const level of levelList) {
        levels[level.id] = level;
      }
      return levels;
    }
  }
  return state;
}

function parseLevel(data) {
  const level = {
    id: data['level'],
    credits: data['credits'],
  };
  return level;
}
