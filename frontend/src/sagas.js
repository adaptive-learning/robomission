import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';

// import * as actionType from './action/types';
import * as api from './api';

// worker Saga: will be fired on USER_FETCH_REQUESTED actions
function* fetchWorld(action) {
   try {
      const world = yield call(api.fetchWorld);
      yield put({type: 'FETCH_WORLD_FULFILLED', data: world});
   } catch (e) {
      yield put({type: 'FETCH_WORLD_FAILED', message: e.message});
   }
}


function* rootSaga() {
  yield takeLatest('FETCH_WORLD_REQUESTED', fetchWorld);
}

export default rootSaga;
