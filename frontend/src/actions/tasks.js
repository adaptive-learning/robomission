import axios from 'axios';

const tasksApiUrl = '/api/tasks/';

export function fetchTasks() {
  return {
    type: 'FETCH_TASKS',
    payload: axios.get(tasksApiUrl),
  }
}
