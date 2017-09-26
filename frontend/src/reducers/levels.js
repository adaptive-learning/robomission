import { FETCH_STATIC_DATA_FULFILLED } from '../action-types';

export default function reduceLevels(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
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
    id: data['level_id'],
    credits: data['credits'],
  };
  return level;
}
