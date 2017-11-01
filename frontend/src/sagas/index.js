import { delay } from 'redux-saga'
import { all, call, cancel, fork, put, select, take, takeEvery, takeLatest } from 'redux-saga/effects';
import * as api from '../api';
import * as actions from '../actions';
import * as actionType from '../action-types';
import { getCurrentUserUrl } from '../selectors/api';
import { getStudentUrl, getPracticeOverviewUrl } from '../selectors/student';
import { getTaskById } from '../selectors/task';
import { getTaskId,
         getTaskSessionId,
         getRoboAst,
         getCode,
         getLengthLimit,
         getEditorType,
         getTaskSourceText,
         isInterpreting } from '../selectors/taskEnvironment';
import { getColor, getPosition, isSolved, isDead, getGameStage } from '../selectors/gameState';
import { interpretRoboAst, interpretRoboCode, InterpreterError } from '../core/roboCodeInterpreter';


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


function* watchTasks(dispatch, getState) {
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
    const newFlow = yield fork(taskFlow, dispatch, getState, taskEnvironmentId, task);
    openTaskFlows[taskEnvironmentId] = newFlow;
    console.log('openTaskFlows:', openTaskFlows);
  }
}


// TODO: Rewrite this saga without calling dispatch and getState;
//       then remove these two parameters.
function* taskFlow(dispatch, getState, taskEnvironmentId, task) {
  console.log('task flow', taskEnvironmentId);
  while (true) {
    const action = yield take([actionType.RUN_PROGRAM, actionType.DO_ACTION_MOVE]);
    if (action.payload.taskEnvironmentId !== taskEnvironmentId) {
      continue;
    }
    if (action.type == actionType.DO_ACTION_MOVE) {
      console.log(action);
      yield put(actions.doAction(taskEnvironmentId, action.payload.action));
      //yield call(delay, 200);
      yield put(actions.move(taskEnvironmentId));
      //yield call(delay, 200);
      yield put(actions.evolveWorld(taskEnvironmentId));
    }
    if (action.type == actionType.RUN_PROGRAM) {
      console.log(action);
      // TODO: check length limit, editor type, finish interpreation, report, allow cancelation
      const roboAst = yield select(getRoboAst, taskEnvironmentId);
      console.log(roboAst);
      yield put(actions.interpretationStarted(taskEnvironmentId));
      const context = {
        doActionMove: (action) => dispatch(actions.doActionMove(taskEnvironmentId, action)),
        color: () => getColor(getState(), taskEnvironmentId),
        position: () => getPosition(getState(), taskEnvironmentId),
        isSolved: () => isSolved(getState(), taskEnvironmentId),
        isDead: () => isDead(getState(), taskEnvironmentId),
        interrupted: () => getGameStage(getState(), taskEnvironmentId) === 'initial',
      };
      interpretRoboAst(roboAst, context);
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


// TODO: Rewrite all sagas without need for dispatch and getState;
//       then remove these two parameters.
function* rootSaga(dispatch, getState) {
  yield all([
    initializeApp(),
    watchActions(),
    watchTasks(dispatch, getState),
  ]);
}

export default rootSaga;
