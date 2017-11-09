// Sagas for all Google Analytics tracking.

import ReactGA from 'react-ga';
import { call, select, takeEvery } from 'redux-saga/effects';

import * as actionType from '../action-types';
import { getTaskId } from '../selectors/taskEnvironment';


function* initGoogleAnalytics() {
  const trackingId = 'UA-81667720-1';
  yield call(ReactGA.initialize, trackingId, { debug: false, titleCase: false });
}


function* reportPageView(action) {
  const { pathname, search } = action.payload;
  const page = pathname + search;
  yield call(ReactGA.set, { page });
  yield call(ReactGA.pageview, page);
}


function* reportProgramExecution(action) {
  const { taskEnvironmentId } = action.payload;
  const taskName = yield select(getTaskId, taskEnvironmentId);
  yield call(ReactGA.event, {
    category: 'Student',
    action: 'Run Program',
    label: taskName,
  });
}


function* reportTaskImport(action) {
  yield call(ReactGA.event, {
    category: 'Student',
    action: 'Import Task',
  });
}


function* reportTaskExport(action) {
  yield call(ReactGA.event, {
    category: 'Student',
    action: 'Export Task',
  });
}


function* googleAnalyticsSaga() {
  yield* initGoogleAnalytics();
  yield takeEvery(actionType.CHANGE_LOCATION, reportPageView);
  yield takeEvery(actionType.RUN_PROGRAM_START, reportProgramExecution);
  yield takeEvery(actionType.IMPORT_TASK, reportTaskImport);
  yield takeEvery(actionType.EXPORT_TASK, reportTaskExport);
}


export default googleAnalyticsSaga;
