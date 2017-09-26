import { SOLVE_TASK_FULFILLED,
         SHOW_NEXT_LEVEL_STATUS,
         UPDATE_STUDENT_FULFILLED } from '../action-types';

const initial = {
  shownLevelStatus: null,
  targetLevelStatus: null,
};

export default function reducePractice(state = initial, action) {
  switch (action.type) {
    case UPDATE_STUDENT_FULFILLED:
      return {
        ...state,
        shownLevelStatus: {
          level: action.payload.level,
          activeCredits: action.payload.activeCredits,
        },
        targetLevelStatus: {
          level: action.payload.level,
          activeCredits: action.payload.activeCredits,
        },
      };
    case SOLVE_TASK_FULFILLED:
      return {
        ...state,
        // shownLevelStatus: state.targetLevelStatus,
        targetLevelStatus: action.payload.progress,
      };
    case SHOW_NEXT_LEVEL_STATUS:
      return {
        ...state,
        shownLevelStatus: action.payload,
      };
    default:
      return state;
  }
}
