import { FETCH_STUDENT_SUCCESS,
         RUN_PROGRAM_SOLVED_REPORT } from '../action-types';


export default function reduceStudent(state = {}, action) {
  switch (action.type) {
    case FETCH_STUDENT_SUCCESS:
      return {
        ...state,
        level: action.payload.level,
        credits: action.payload.credits,
        activeCredits: action.payload.activeCredits,
        practiceOverviewUrl: action.payload.practiceOverviewUrl,
        startTaskUrl: action.payload.startTaskUrl,
        watchInstructionUrl: action.payload.watchInstructionUrl,
        reportProgramEditUrl: action.payload.reportProgramEditUrl,
        reportProgramExecutionUrl: action.payload.reportProgramExecutionUrl,
      };
    case RUN_PROGRAM_SOLVED_REPORT:
      return {
        ...state,
        level: action.payload.progress.level,
        credits: action.payload.progress.credits,
        activeCredits: action.payload.progress.activeCredits,
      };
    default:
      return state;
  }
}
