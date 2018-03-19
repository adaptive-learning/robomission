import { FETCH_STUDENT_SUCCESS,
         FETCH_PRACTICE_OVERVIEW_SUCCESS } from '../action-types';


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
    case FETCH_PRACTICE_OVERVIEW_SUCCESS:
      return {
        ...state,
        mission: action.payload.mission,
        phase: action.payload.phase,
      };
    default:
      return state;
  }
}
