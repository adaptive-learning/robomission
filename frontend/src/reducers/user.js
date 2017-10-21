import { FETCH_USER_SUCCESS } from '../action-types';


export default function reduceUser(state = {}, action) {
  switch (action.type) {
    case FETCH_USER_SUCCESS:
      return {
        ...state,
        student_url: action.payload.studentUrl,
      };
    default:
      return state;
  }
}
