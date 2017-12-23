import {take, call, put, fork} from 'redux-saga/effects';
import * as authApi from '../api/auth';
import * as actions from '../actions';
import * as actionType from '../action-types';


export function* signUpFlow () {
  while (true) {
    const action = yield take(actionType.SIGNUP_REQUEST)
    const { credentials, profile } = action.payload;
    try {
      yield call(authApi.signUp, credentials);
      yield call(authApi.updateProfile, profile);
      yield put(actions.signUp.success());
      yield put(actions.login.success());
    } catch (error) {
      yield put(actions.signUp.failure(error.fieldErrors));
    }
  }
}


export function* loginFlow () {
  while (true) {
    const action = yield take(actionType.LOGIN_REQUEST)
    const { credentials, provider } = action.payload;
    try {
      if (provider === 'facebook') {
        yield call(authApi.loginViaFacebook);
      } else if (provider === 'google') {
        yield call(authApi.loginViaGoogle);
      } else {
        yield call(authApi.login, credentials);
      }
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
      // To make sure there are absolutely no leftovers in the state after the
      // logout, the page is reloaded.
      window.location.href = '/';
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
