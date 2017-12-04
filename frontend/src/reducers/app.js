import { CHANGE_LOCATION,
         FETCH_WORLD_SUCCESS,
         FETCH_PRACTICE_OVERVIEW_REQUEST,
         FETCH_PRACTICE_OVERVIEW_SUCCESS,
         EDIT_PROGRAM_AST,
         EDIT_PROGRAM_CODE,
         TOGGLE_LOGIN_MODAL,
         TOGGLE_SIGNUP_MODAL,
         FETCH_STUDENT_SUCCESS,
         LOGIN_FAILURE,
         LOGIN_SUCCESS,
         SIGNUP_FAILURE } from '../action-types';


const initial = {
  mode: 'intro',
  staticDataLoaded: false,
  studentLoaded: false,
  practiceOverviewLoaded: false,
  practiceOverviewInvalidated: false,
  isLoginModalOpen: false,
  isSignUpModalOpen: false,
  signUpModalErrors: {},
  loginFailed: false,
};


export default function reduceApp(state = initial, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS:
      return {
        ...state,
        staticDataLoaded: true,
      };
    case FETCH_STUDENT_SUCCESS:
      return {
        ...state,
        studentLoaded: true,
      };
    case FETCH_PRACTICE_OVERVIEW_REQUEST:
      return {
        ...state,
        practiceOverviewLoaded: false,
      };
    case FETCH_PRACTICE_OVERVIEW_SUCCESS:
      return {
        ...state,
        practiceOverviewLoaded: true,
        practiceOverviewInvalidated: false,
      };
    case EDIT_PROGRAM_AST:
    case EDIT_PROGRAM_CODE:
      // whenever a code is changed, solving time is updated
      return {
        ...state,
        practiceOverviewInvalidated: true,
      };
    case CHANGE_LOCATION:
      return {
        ...state,
        mode: getMode(action.payload.pathname),
      };
    case TOGGLE_LOGIN_MODAL:
      return {
        ...state,
        isLoginModalOpen: action.payload.open,
      };
    case LOGIN_FAILURE:
      return {
        ...state,
        loginFailed: true,
      };
    case LOGIN_SUCCESS:
      return {
        ...state,
        isSignUpModalOpen: false,
        isLoginModalOpen: false,
        loginFailed: false,
      };
    case TOGGLE_SIGNUP_MODAL:
      return {
        ...state,
        isSignUpModalOpen: action.payload.open,
      };
    case SIGNUP_FAILURE:
      return {
        ...state,
        signUpModalErrors: action.payload.fieldErrors,
      };
    default:
      return state;
  }
}


function getMode(path) {
  const parts = path.split('/');
  const topPage = parts[1];
  const mode = (!topPage) ? 'intro' : topPage;
  return mode;
}
