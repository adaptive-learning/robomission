import { UPDATE_STUDENT_FULFILLED,
         SOLVE_TASK_FULFILLED } from '../action-types';


export default function reduceStudent(state = {}, action) {
  switch (action.type) {
    case UPDATE_STUDENT_FULFILLED:
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
    case SOLVE_TASK_FULFILLED:
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
