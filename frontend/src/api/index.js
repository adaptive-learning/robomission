/**
 * Defines the interface between the backend and the frontend.
 */
import axios from 'axios';
import { API_PATH } from '../config';


export function fetchApiRoot() {
  return axios.get(API_PATH).then(response => ({
    apiRoot: parseApiRoot(response.data),
  }));
}


function parseApiRoot(data) {
  return {
    // hack to make cookies work correctly
    // TODO: fix it to allow for data['current_user']
    currentUserUrl: `${API_PATH}/users/current/`, // relativizeUrl(data['current_user']),
    worldUrl: relativizeUrl(data['domain']),

    // Hack to make feedback work after it was moved under monitoring API.
    // TODO(refactor): merge learn and monitoring API
    feedbackUrl: '/monitoring/api/feedback/',
  }
}


export function fetchWorld(url) {
  // TODO: hoist world parsing from reducers to this api module
  return axios.get(url).then(response => response.data);
}


export function fetchUser(url) {
  return axios.get(url).then(response => ({
    studentUrl: relativizeUrl(response.data['student']),
    teacherUrl: relativizeUrl(response.data['teacher']),
    email: response.data['email'],
    nickname: response.data['nickname'],
    isStaff: response.data['is_staff'],
    isLazy: response.data['is_lazy'],
    created: response.data['created'],
  }));
}


export function fetchStudent(url) {
  return axios.get(url).then(response => {
    const { data } = response;
    return {
      credits: data['credits'],
      activeCredits: data['active_credits'],
      level: data['level'],
      seenInstructions: data['seen_instructions'],
      practiceOverviewUrl: relativizeUrl(data['practice_overview']),
      watchInstructionUrl: relativizeUrl(data['watch_instruction']),
      startTaskUrl: relativizeUrl(data['start_task']),
      reportProgramEditUrl: relativizeUrl(data['edit_program']),
      reportProgramExecutionUrl: relativizeUrl(data['run_program']),
    };
  });
}


export function fetchPracticeOverview(url) {
  return axios.get(url).then(response => {
    const { data } = response;
    return {
      level: data['level'],
      credits: data['credits'],
      tasks: data['tasks'],
      recommendation: data['recommendation'],
    };
  });
}


export function seeInstruction(url, instructionId) {
  const data = { 'instruction': instructionId };
  return axios.post(url, data);
}


export function startTask(url, taskId) {
  const data = { 'task': taskId };
  return axios.post(url, data).then(response => parseStartTask(response.data));
}


function parseStartTask(data) {
  return {
    taskSessionId: data['task_session_id'],
  };
}


export function reportProgramEdit(url, taskSessionId, newMiniCode) {
  const data = {
    'task-session-id': taskSessionId,
    'program': newMiniCode,
  };
  return axios.post(url, data);
}


export function reportProgramExecution(url, taskSessionId, miniCode, solved) {
  const data = {
    'task-session-id': taskSessionId,
    'program': miniCode,
    'correct': solved,
  };
  return axios.post(url, data).then(response => parseProgramExecution(response.data));
}


function parseProgramExecution(data) {
  if (!data.correct) {
    return { solved: false };
  }
  return {
    solved: true,
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


export function sendFeedback(feedbackUrl, comment, email, url) {
  const data = { comment, email, url };
  return axios.post(feedbackUrl, data)
    .catch(error => {
      const { data } = error.response;
      error.fieldErrors = {
        email: (data.email) ? data.email[0] : null,
        comment: (data.comment) ? data.comment[0] : null,
      };
      throw error;
    });
}


function relativizeUrl(url) {
  // During development, use only the relative path of the url. This is
  // currently necessary during FE development, when there are separate FE and
  // BE server running on different ports. This transformation makes sure that
  // the absolute URLs passed by the BE will be treated the same way as the
  // relative urls hardcoded in the FE (i.e. they will be proxied from FE port
  // 3000 to the BE port 8000, as set in the package.json) and so they will use
  // same set of cookies. (As a side benefit, it also means that we don't have
  // to care about cross-site requests during development.)
  // TODO: Find a better solution for the missing-cookies-with-different-ports
  // problem. This works, but is error prone, e.g. it's easy to forget
  // relativize a new url and it increases a discrepancy between development
  // and production (which will use some relative and some absolute URLs).
  if (!url) {
    return url;
  }
  const parts = url.split('localhost:8000');
  if (parts.length === 2) {
    return parts[1];
  }
  return url;
}
