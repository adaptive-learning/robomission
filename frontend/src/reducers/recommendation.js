import { FETCH_PRACTICE_OVERVIEW_SUCCESS,
         RUN_PROGRAM_SOLVED_REPORT } from '../action-types';

const initial = {
  available: false,
};

export default function reduceRecommendation(state = initial, action) {
  switch (action.type) {
    case FETCH_PRACTICE_OVERVIEW_SUCCESS:
      return parseRecommendation(action.payload.recommendation);
    case RUN_PROGRAM_SOLVED_REPORT:
      return parseRecommendation(action.payload.recommendation);
    default:
      return state;
  }
}


function parseRecommendation(data) {
  return {
    available: data['available'],
    task: data['task'],
    phase: data['phase'],
    mission: data['mission'],
  };
}
