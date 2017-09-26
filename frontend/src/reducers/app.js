import { LOCATION_CHANGE } from 'react-router-redux';
import { FETCH_STATIC_DATA_FULFILLED,
         FETCH_PRACTICE_OVERVIEW_FULFILLED,
         FETCH_PRACTICE_OVERVIEW_PENDING,
         REPORT_PROGRAM_EDIT_PENDING,
         UPDATE_STUDENT_FULFILLED } from '../action-types';


const initial = {
  mode: 'intro',
  staticDataLoaded: false,
  studentLoaded: false,
  practiceOverviewLoaded: false,
  practiceOverviewInvalidated: false,
};


export default function reduceApp(state = initial, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED:
      return {
        ...state,
        staticDataLoaded: true,
      };
    case UPDATE_STUDENT_FULFILLED:
      return {
        ...state,
        studentLoaded: true,
      };
    case FETCH_PRACTICE_OVERVIEW_PENDING:
      return {
        ...state,
        practiceOverviewLoaded: false,
      };
    case FETCH_PRACTICE_OVERVIEW_FULFILLED:
      return {
        ...state,
        practiceOverviewLoaded: true,
        practiceOverviewInvalidated: false,
      };
    case REPORT_PROGRAM_EDIT_PENDING:
      // whenever a code is changed, solving time is updated
      return {
        ...state,
        practiceOverviewInvalidated: true,
      };
    case LOCATION_CHANGE:
      return {
        ...state,
        mode: getMode(action.payload.pathname),
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
