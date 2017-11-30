import {take, call, put, fork, race} from 'redux-saga/effects';
import * as authApi from '../authApi';
import * as actions from '../actions';
import * as actionType from '../action-types';


export function * signUpFlow () {
  while (true) {
    const action = yield take(actionType.SIGNUP_REQUEST)
    const { credentials, profile } = action.payload;
    try {
      const response = yield call(authApi.signUp, credentials);
      console.log('response', response);
      yield put(actions.signUp.success());
      yield put(actions.login.success());
    } catch (error) {
      yield put(actions.signUp.failure(error));
    }
  }
}

export default function* authSaga () {
  yield fork(signUpFlow)
}
