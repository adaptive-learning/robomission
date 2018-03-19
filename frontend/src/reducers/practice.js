import { RUN_PROGRAM_SOLVED_REPORT,
         SHOW_NEXT_LEVEL_STATUS } from '../action-types';

const initial = {
  progress: null,
};

export default function reducePractice(state = initial, action) {
  switch (action.type) {
    case RUN_PROGRAM_SOLVED_REPORT:
      return {
        ...state,
        progress: action.payload.progress,
      };
    case SHOW_NEXT_LEVEL_STATUS:
      return {
        ...state,
        progress: null,
      };
    default:
      return state;
  }
}
