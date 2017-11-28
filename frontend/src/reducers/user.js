import { FETCH_USER_SUCCESS, CHANGE_CREDENTIALS } from '../action-types';


const emptyCredentials = {
  email: '',
  password: '',
}


const initialState = {
  credentials: emptyCredentials,
}


export default function reduceUser(state = initialState, action) {
  switch (action.type) {
    case FETCH_USER_SUCCESS:
      return {
        ...state,
        studentUrl: action.payload.studentUrl,
      };
    case CHANGE_CREDENTIALS:
      return {
        ...state,
        credentials: action.payload.credentials,
      };
    default:
      return state;
  }
}
