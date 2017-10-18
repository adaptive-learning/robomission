import axios from 'axios';

const tasksApiUrl = '/learn/api/tasks/';

export function fetchTasks() {
  return {
    type: 'FETCH_TASKS',
    payload: axios.get(tasksApiUrl),
  }
}
