import { FETCH_PRACTICE_OVERVIEW_FULFILLED,
         SOLVE_TASK_FULFILLED } from '../action-types';

const initial = {
  available: false,
};

export default function reduceRecommendation(state = initial, action) {
  switch (action.type) {
    case FETCH_PRACTICE_OVERVIEW_FULFILLED:
      return parseRecommendation(action.payload.recommendation);
    case SOLVE_TASK_FULFILLED:
      return parseRecommendation(action.payload.recommendation);
    default:
      return state;
  }
}


function parseRecommendation(data) {
  return {
    available: data['available'],
    task: data['task_id'],
  };
}
