import { FETCH_USER_SUCCESS, CHANGE_NICKNAME, CHANGE_CREDENTIALS } from '../action-types';


const emptyCredentials = {
  email: '',
  password: '',
}


const initialState = {
  credentials: emptyCredentials,
  nickname: '',
}


export default function reduceUser(state = initialState, action) {
  switch (action.type) {
    case FETCH_USER_SUCCESS:
      return {
        ...state,
        ...action.payload,
      };
    case CHANGE_CREDENTIALS:
      return {
        ...state,
        credentials: action.payload.credentials,
      };
    case CHANGE_NICKNAME:
      return {
        ...state,
        nickname: action.payload.nickname,
      };
    default:
      return state;
  }
}
