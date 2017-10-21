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
    studentUrl: response.data['student'],
  }));
}


export function fetchStudent(url) {
  //const url = getStudentUrl(state);
  return axios.get(url).then(response => {
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
  });
}


export function fetchPraticeOverview(url) {
  // const url = getPracticeOverviewUrl(state);
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
