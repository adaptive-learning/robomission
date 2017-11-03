import { RUN_PROGRAM_SOLVED_REPORT,
         SHOW_NEXT_LEVEL_STATUS,
         FETCH_STUDENT_SUCCESS } from '../action-types';

const initial = {
  shownLevelStatus: null,
  targetLevelStatus: null,
};

export default function reducePractice(state = initial, action) {
  switch (action.type) {
    case FETCH_STUDENT_SUCCESS:
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
    case RUN_PROGRAM_SOLVED_REPORT:
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
