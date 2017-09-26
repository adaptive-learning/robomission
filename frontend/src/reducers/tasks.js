import { FETCH_STATIC_DATA_FULFILLED,
         FETCH_PRACTICE_OVERVIEW_FULFILLED } from '../action-types';


export default function reduceTasks(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      const taskList = action.payload.tasks.map(parseTask);
      const tasks = {};
      for (const task of taskList) {
        tasks[task.id] = task;
      }
      return tasks;
    }
    case FETCH_PRACTICE_OVERVIEW_FULFILLED: {
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
  }
  return state;
}

function parseTask(data) {
  const task = {
    id: data['task_id'],
    category: data['category'],
    setting: jsonToObject(data.setting),
    // solution: jsonToObject(data.solution), // TODO: requires to fix json fields first
  };
  return task;
}

function jsonToObject(jsonStr) {
  return JSON.parse(jsonStr.replace(/'/g, '"'));
}


function parseStudentTask(data) {
  const task = {
    id: data['task_id'],
    solved: data['solved'],
    time: data['time'],
  };
  return task;
}
