import { FETCH_API_ROOT_SUCCESS } from '../action-types';


export default function reduceStudent(state = {}, action) {
  switch (action.type) {
    case FETCH_API_ROOT_SUCCESS:
      return {
        ...state,
        ...action.payload.apiRoot,
      };
    default:
      return state;
  }
}
