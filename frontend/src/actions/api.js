/**
 * Api for communication with the backend
 */
import axios from 'axios';
import { FETCH_STATIC_DATA,
         FETCH_PRACTICE_OVERVIEW,
         UPDATE_STUDENT,
         START_SESSION,
         START_TASK,
         SOLVE_TASK,
         SEE_INSTRUCTION } from '../action-types';
import { generateMiniRoboCode } from '../core/miniRoboCodeGenerator';


export function fetchStaticData() {
  const entityNames = ['blocks', 'toolboxes', 'tasks', 'levels', 'instructions'];
  const urls = entityNames.map(name => `/learn/api/${name}`);
  const requests = urls.map(url => axios.get(url));
  return {
    type: FETCH_STATIC_DATA,
    payload: axios.all(requests).then(results => {
      const namedResults = {};
      for (const [i, name] of entityNames.entries()) {
        namedResults[name] = results[i].data;
      }
      return namedResults;
    }),
  };
}


export function startSession() {
  return dispatch => {
    const action = {
      type: START_SESSION,
      payload: getOrCreateUser().then(parseUserResponse),
    };
    return dispatch(action)
      .then(() => dispatch(updateStudent()))
      .then(() => dispatch(fetchPraticeOverview()));
  };
}


function getOrCreateUser() {
  // TODO: should be post (but it requires BE change)
  return axios.get('/learn/api/users/current');
}


function parseUserResponse(response) {
  const data = response.data;
  return {
    student_url: data['student'],
  };
}


// TODO: factor out non-api (taskEnvironment) part
export function startTask(taskId, taskEnvironmentId) {
  return (dispatch, getState) => {
    const state = getState();
    const { startTaskUrl } = state.student;
    const data = { 'task': taskId };
    const action = {
      type: START_TASK,
      payload: axios.post(startTaskUrl, data)
        .then(parseStartTaskResponse)
        .then(payload => ({ ...payload, taskEnvironmentId })),
    };
    return dispatch(action);
  };
}


export function reportProgramEdit(taskSessionId, oldAst, newAst) {
  return (dispatch, getState) => {
    const editProgramUrl = getReportProgramEditUrl(getState());
    const oldMiniCode = generateMiniRoboCode(oldAst);
    const newMiniCode = generateMiniRoboCode(newAst);
    if (oldMiniCode === newMiniCode) {
      return;
    }
    const data = {
      'task-session-id': taskSessionId,
      'program': newMiniCode,
    };
    const action = {
      type: 'REPORT_PROGRAM_EDIT',
      payload: axios.post(editProgramUrl, data),
    };
    dispatch(action);
  };
}


// TODO: factor out non-api (taskEnvironment) part
export function reportProgramExecution(taskSessionId, program, solved, taskEnvironmentId) {
  return (dispatch, getState) => {
    const runProgramUrl = getReportProgramExecutionUrl(getState());
    const shortProgram = generateMiniRoboCode(program);
    const data = {
      'task-session-id': taskSessionId,
      'program': shortProgram,
      'correct': solved,
    };
    if (solved) {
      const action = {
        type: SOLVE_TASK,
        payload: axios.post(runProgramUrl, data)
          .then(parseSolveTaskResponse)
          .then(payload => ({ ...payload, taskEnvironmentId })),
      };
      return dispatch(action);
    }
    const action = {
      type: 'REPORT_INCORRECT_PROGRAM_EXECUTION',
      payload: axios.post(runProgramUrl, data),
    };
    // TODO: maybe it's not even needed to dispatch any action for incorrect runs?
    return dispatch(action);
  };
}


export function seeInstruction(instructionId) {
  return (dispatch, getState) => {
    const state = getState();
    const { watchInstructionUrl } = state.student;
    const data = { 'instruction': instructionId };
    const action = {
      type: SEE_INSTRUCTION,
      payload: {
        promise: axios.post(watchInstructionUrl, data),
        data: { instructionId },
      },
    };
    return dispatch(action);
  };
}


function postAction(type, data = {}) {
  throw new Error("Posting actions directly is not supported anymore.");
  //const requestData = {
  //  type,
  //  data: JSON.stringify(data),
  //};
  //return axios.post('/api/actions/', requestData);
}


function parseStartTaskResponse(response) {
  const { data } = response;
  return {
    taskSessionId: data['task_session_id'],
  };
}


function parseSolveTaskResponse(response) {
  const data = response.data;
  return {
    recommendation: data['recommendation'],
    progress: parseProgress(data['progress']),
  };
}


function parseProgress(data) {
  return {
    level: data['level'],
    credits: data['credits'],
    activeCredits: data['active_credits'],
  };
}


function updateStudent() {
  return (dispatch, getState) => dispatch({
    type: UPDATE_STUDENT,
    payload: axios.get(getStudentUrl(getState())).then(parseStudentResponse),
  });
}


export function fetchPraticeOverview() {
  return (dispatch, getState) => dispatch({
    type: FETCH_PRACTICE_OVERVIEW,
    payload: axios.get(getPracticeOverviewUrl(getState())).then(parsePracticeOverviewResponse),
  });
}


// TODO: move to selectors
function getStudentUrl(state) {
  return state.user.student_url;
}

function getPracticeOverviewUrl(state) {
  return state.student.practiceOverviewUrl;
}

function getSolveTaskUrl(state) {
  return state.student.solveTaskUrl;
}

function getReportProgramExecutionUrl(state) {
  return state.student.reportProgramExecutionUrl;
}

function getReportProgramEditUrl(state) {
  return state.student.reportProgramEditUrl;
}

function parseStudentResponse(response) {
  const { data } = response;
  return {
    credits: data['credits'],
    activeCredits: data['active_credits'],
    level: data['level'],
    seenInstructions: data['seen_instructions'],
    practiceOverviewUrl: data['practice_overview'],
    watchInstructionUrl: data['watch_instruction'],
    startTaskUrl: data['start_task'],
    reportProgramEditUrl: data['edit_program'],
    reportProgramExecutionUrl: data['run_program'],
  };
}


function parsePracticeOverviewResponse(response) {
  const { data } = response;
  return {
    level: data['level'],
    credits: data['credits'],
    activeCredits: data['active_credits'],
    tasks: data['tasks'],
    recommendation: data['recommendation'],
  };
}
