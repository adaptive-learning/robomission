export function isLoaded(state) {
  return state.app.staticDataLoaded && state.app.studentLoaded && state.app.practiceOverviewLoaded;
}


export function isPracticeOverviewInvalidated(state) {
  return state.app.practiceOverviewInvalidated;
}

export function inMode(state, mode) {
  // TODO: check that mode is one of the valid modes
  return getMode(state) === mode;
}


export function getMode(state) {
  return state.app.mode;
}


export function isLoginModalOpen(state) {
  return state.app.isLoginModalOpen;
}


export function getLoginFailed(state) {
  return state.app.loginFailed;
}


export function isSignUpModalOpen(state) {
  return state.app.isSignUpModalOpen;
}


export function getSignUpModalErrors(state) {
  return state.app.signUpModalErrors;
}


export function getSnackbarMessageId(state) {
  return state.app.snackbarMessageId;
}
