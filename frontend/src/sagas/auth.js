import {take, call, put, fork} from 'redux-saga/effects';
import * as authApi from '../authApi';
import * as actions from '../actions';
import * as actionType from '../action-types';


export function * signUpFlow () {
  while (true) {
    const action = yield take(actionType.SIGNUP_REQUEST)
    const { credentials, profile } = action.payload;
    try {
      yield call(authApi.signUp, credentials);
      yield call(authApi.updateProfile, profile);
      yield put(actions.signUp.success());
      yield put(actions.login.success());
    } catch (error) {
      yield put(actions.signUp.failure(error));
    }
  }
}


export function* loginFlow () {
  while (true) {
    const action = yield take(actionType.LOGIN_REQUEST)
    const { credentials } = action.payload;
    try {
      yield call(authApi.login, credentials);
      yield put(actions.login.success());
    } catch (error) {
      yield put(actions.login.failure(error));
    }
  }
}


export function* logoutFlow () {
  while (true) {
    yield take(actionType.LOGOUT_REQUEST)
    try {
      yield call(authApi.logout);
      yield put(actions.logout.success());
    } catch (error) {
      yield put(actions.logout.failure(error));
    }
  }
}


export default function* authSaga () {
  yield fork(signUpFlow);
  yield fork(loginFlow);
  yield fork(logoutFlow);
}
