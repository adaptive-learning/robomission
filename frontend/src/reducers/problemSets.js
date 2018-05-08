import { FETCH_WORLD_SUCCESS,
         FETCH_PRACTICE_OVERVIEW_SUCCESS,
         SHOW_NEXT_LEVEL_STATUS} from '../action-types';

export default function reduceProblemSets(state = {}, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
      const psList = action.payload.problemsets.map(parseProblemSet);
      const problemSets = {};
      for (const ps of psList) {
        problemSets[ps.id] = ps;
      }
      return problemSets;
    }
    case FETCH_PRACTICE_OVERVIEW_SUCCESS: {
      const problemSets = {};
      for (const skill of action.payload.skills) {
        problemSets[skill.name] = {
          ...state[skill.name],
          skill: skill.value,
        };
      }
      return problemSets;
    }
    case SHOW_NEXT_LEVEL_STATUS:
      const problemSets = {...state};
      for (const progress of action.payload.progress) {
        problemSets[progress.chunk] = {
          ...state[progress.chunk],
          skill: progress.skill,
        };
      }
      return problemSets;
    default: {
      return state;
    }
  }
}

function parseProblemSet(data) {
  const ps = {
    id: data['name'],
    granularity: data['granularity'],
    section: data['section'],
    level: data['level'],
    order: data['order'],
    setting: data['setting'],
    tasks: data['tasks'],
    parts: data['parts'],
    parent: data['parent'],
  };
  return ps;
}
