import { getNextLevelStatus } from '../selectors/practice';
import { SHOW_NEXT_LEVEL_STATUS } from '../action-types';


export function showLevelProgress() {
  return (dispatch, getState) => {
    const state = getState();
    const nextLevelStatus = getNextLevelStatus(state);
    if (nextLevelStatus === null) {
      return;
    }
    dispatch(showNextLevelStatus(nextLevelStatus));
  };
}


function showNextLevelStatus(levelStatus) {
  return {
    type: SHOW_NEXT_LEVEL_STATUS,
    payload: levelStatus,
  };
}
