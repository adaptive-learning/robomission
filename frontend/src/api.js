/**
 * Defines the interface between the backend and the frontend.
 */
import axios from 'axios';
import { API_PATH } from './config';
import { getStudentUrl, getPracticeOverviewUrl } from './selectors/student';


export function fetchWorld() {
  const entityNames = ['blocks', 'toolboxes', 'tasks', 'levels', 'instructions'];
  const urls = entityNames.map(name => `${API_PATH}/${name}`);
  const requests = urls.map(url => axios.get(url));
  return axios.all(requests).then(results => {
    const namedResults = {};
    for (const [i, name] of entityNames.entries()) {
      namedResults[name] = results[i].data;
    }
    return namedResults;
  });
}


export function fetchUser() {
  return axios.get(`${API_PATH}/users/current`).then(response => ({
    studentUrl: relativizeUrl(response.data['student']),
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


export function fetchPraticeOverview(url) {
  return axios.get(url).then(response => {
    const { data } = response;
    return {
      level: data['level'],
      credits: data['credits'],
      activeCredits: data['active_credits'],
      tasks: data['tasks'],
      recommendation: data['recommendation'],
    };
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
  const parts = url.split('localhost:8000');
  if (parts.length == 2) {
    return parts[1];
  }
  return url;
}
