import {call, put, takeLatest} from 'redux-saga/effects';
import * as api from '../api/monitoring';
import * as actions from '../actions/monitoring';
import * as actionType from '../action-types';


function* fetchMetrics(action) {
  try {
    const metrics = yield call(api.fetchMetrics);
    yield put(actions.fetchMetrics.success(metrics));
  } catch (error) {
    yield put(actions.fetchMetrics.failure(error));
  }
}


export default function* monitoringSaga () {
  yield takeLatest(actionType.FETCH_METRICS_REQUEST, fetchMetrics);
}
