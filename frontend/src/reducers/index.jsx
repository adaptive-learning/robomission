import { practiceReducer } from './practiceReducer';
import { taskSessionReducer } from './taskSessionReducer';
import { tasksReducer } from './tasksReducer';
import menuReducer from './menu';

const reducers = {
  tasks: tasksReducer,
  taskSession: taskSessionReducer,
  practice: practiceReducer,
  menu: menuReducer,
};

export default reducers;
