import { delay } from 'redux-saga'
import { all, call, cancel, fork, put, select, take, takeEvery, takeLatest } from 'redux-saga/effects';
import * as api from '../api';
import * as actions from '../actions';
import * as actionType from '../action-types';
import { getCurrentUserUrl } from '../selectors/api';
import { getStudentUrl, getPracticeOverviewUrl } from '../selectors/student';
import { getTaskById } from '../selectors/task';


function* fetchApiRoot() {
  try {
    const apiRoot = yield call(api.fetchApiRoot);
    yield put(actions.fetchApiRoot.success(apiRoot));
  } catch (error) {
    yield put(actions.fetchApiRoot.failure(error));
  }
}


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
    const user = yield call(api.fetchUser, action.payload.url);
    yield put(actions.fetchUser.success(user));
  }
  catch (error) {
    yield put(actions.fetchUser.failure(error));
  }
}


function* fetchStudent(action) {
  try {
    const { url } = action.payload;
    const student = yield call(api.fetchStudent, url);
    yield put(actions.fetchStudent.success(student));
  } catch (error) {
    yield put(actions.fetchStudent.failure(error));
  }
}


function* fetchPracticeOverview(action) {
  try {
    const { url } = action.payload;
    const practiceOverview = yield call(api.fetchPracticeOverview, url);
    yield put(actions.fetchPracticeOverview.success(practiceOverview));
  } catch (error) {
    yield put(actions.fetchPracticeOverview.failure(error));
  }
}


function* watchTasks() {
  const openTaskFlows = {};
  while (true) {
    const action = yield take(actionType.SET_TASK);
    const { taskEnvironmentId, task } = action.payload;
    const oldFlow = openTaskFlows[taskEnvironmentId];
    if (oldFlow) {
      console.log('closing old flow');
      yield cancel(oldFlow);
    }
    console.log('forking new flow');
    const newFlow = yield fork(taskFlow, taskEnvironmentId, task);
    openTaskFlows[taskEnvironmentId] = newFlow;
    console.log('openTaskFlows:', openTaskFlows);
  }
}


function* taskFlow(taskEnvironmentId, task) {
  console.log('task flow', taskEnvironmentId);
  while (true) {
    const action = yield take(actionType.DO_ACTION_MOVE);
    if (action.payload.taskEnvironmentId === taskEnvironmentId) {
      console.log(action);
      yield put(actions.doAction(taskEnvironmentId, action.payload.action));
      //yield call(delay, 200);
      yield put(actions.move(taskEnvironmentId));
      //yield call(delay, 200);
      yield put(actions.evolveWorld(taskEnvironmentId));
    }
  }
}


// Intercept setTask action to add complete task record
// (which is currently required by some reducers).
function* setTask(action) {
  const { taskEnvironmentId, taskId } = action.payload;
  const task = yield select(getTaskById, taskId);
  const setTaskAction = actions.setTask(taskEnvironmentId, task);
  yield put(setTaskAction);
}


function* initializeApp() {
  yield* fetchApiRoot();
  yield* fetchWorld();
  const currentUserUrl = yield select(getCurrentUserUrl);
  yield* fetchUser(actions.fetchUser.request(currentUserUrl));

  const studentUrl = yield select(getStudentUrl);
  yield* fetchStudent(actions.fetchStudent.request(studentUrl));

  const practiceOverviewUrl = yield select(getPracticeOverviewUrl);
  const practiceOverviewAction = actions.fetchPracticeOverview.request(practiceOverviewUrl);
  yield* fetchPracticeOverview(practiceOverviewAction);
}


function* watchActions() {
  yield takeLatest(actionType.FETCH_STUDENT_REQUEST, fetchStudent);
  yield takeLatest(actionType.FETCH_PRACTICE_OVERVIEW_REQUEST, fetchPracticeOverview);
  yield takeEvery(actionType.SET_TASK_BY_ID, setTask);
}


function* rootSaga() {
  yield all([
    initializeApp(),
    watchActions(),
    watchTasks(),
  ]);
}

export default rootSaga;
