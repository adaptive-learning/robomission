import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';

import * as api from '../api';
import * as actions from '../actions';
import * as actionType from '../action-types';


function* fetchWorld() {
   try {
      const world = yield call(api.fetchWorld);
      yield put(actions.fetchWorld.success(world));
   } catch (error) {
      yield put(actions.fetchWorld.failure(error));
   }
}


function* fetchUser(action) {
   try {
      const user = yield call(api.fetchUser);
      yield put(actions.fetchUser.success(user));
   } catch (error) {
      yield put(actions.fetchUser.failure(error));
   }
}


function* rootSaga() {
  yield* fetchWorld();
  yield* fetchUser();
  //yield takeLatest(actionType.FETCH_USER_REQUEST, fetchUser);
}

export default rootSaga;
