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
