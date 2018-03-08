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
      // Inject task chunks.
      for (const chunk of action.payload.chunks) {
        for (const taskId of chunk.tasks) {
          tasks[taskId].chunk = chunk.name;
        }
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
    category: data['level'],  // TODO: rename category to level
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
    id: data['name'],
    solved: data['solved'],
    time: data['time'],
  };
  return task;
}
