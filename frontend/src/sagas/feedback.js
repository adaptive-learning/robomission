// Sagas for user feedback processing.
import { call, put, select, takeLatest } from 'redux-saga/effects';
import * as actionType from '../action-types';
import * as actions from '../actions';
import * as api from '../api';
import { getFeedbackUrl } from '../selectors/api';


function* submitFeedback(action) {
  const { feedback, url } = action.payload;
  const { comment, email } = feedback;
  const feedbackUrl = yield select(getFeedbackUrl);
  try {
    yield call(api.sendFeedback, feedbackUrl, comment, email, url);
    yield put(actions.submitFeedback.success());
  }
  catch (error) {
    yield put(actions.submitFeedback.failure(error));
  }
}


function* feedbackSaga() {
  yield takeLatest(actionType.SUBMIT_FEEDBACK_REQUEST, submitFeedback);
}


export default feedbackSaga;
