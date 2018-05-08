import { FETCH_WORLD_SUCCESS,
         FETCH_PRACTICE_OVERVIEW_SUCCESS } from '../action-types';


export default function reduceTasks(state = {}, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
      const taskList = action.payload.tasks.map(parseTask);
      const tasks = {};
      for (const task of taskList) {
        tasks[task.id] = task;
      }
      return tasks;
    }
    case FETCH_PRACTICE_OVERVIEW_SUCCESS: {
      const taskList = action.payload.tasks.map(parseStudentTask);
      const tasks = {};
      // TODO: more safe and expressive way of merging tasks with student-tasks
      for (const task of taskList) {
        tasks[task.id] = {
          ...state[task.id],
          ...task,
        };
      }
      return tasks;
    }
    default: {
      return state;
    }
  }
}

function parseTask(data) {
  const task = {
    id: data['name'],
    category: data['level'],  // TODO: remove once not needed
    level: data['level'],
    levels: data['levels'],
    order: data['order'],
    problemSet: data['problemset'],
    setting: data.setting,
  };
  return task;
}

function parseStudentTask(data) {
  const task = {
    id: data['name'],
    solved: data['solved'],
    time: data['time'],
  };
  return task;
}
