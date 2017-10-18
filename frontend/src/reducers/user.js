import { START_SESSION_FULFILLED } from '../action-types';


export default function reduceUser(state = {}, action) {
  switch (action.type) {
    case START_SESSION_FULFILLED:
      return {
        ...state,
        student_url: action.payload.student_url,
      };
    default:
      return state;
  }
}
