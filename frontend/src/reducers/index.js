import { combineReducers } from 'redux';
import { intlReducer } from 'react-intl-redux';
import { routerReducer } from 'react-router-redux';
import reduceApp from './app';
import reduceBlocks from './blocks';
import reduceCategories from './categories';
import reduceInstructions from './instructions';
import reduceLevels from './levels';
import reduceTasks from './tasks';
import reduceToolboxes from './toolboxes';
import reduceStudent from './student';
import reduceRecommendation from './recommendation';
import reduceMenu from './menu';
import reduceTaskEnvironments from './taskEnvironments';
import reduceTaskEditor from './taskEditor';
import reducePractice from './practice';


export const reducers = combineReducers({
  app: reduceApp,
  blocks: reduceBlocks,
  categories: reduceCategories,
  instructions: reduceInstructions,
  levels: reduceLevels,
  tasks: reduceTasks,
  toolboxes: reduceToolboxes,
  student: reduceStudent,
  recommendation: reduceRecommendation,
  menu: reduceMenu,
  taskEnvironments: reduceTaskEnvironments,
  taskEditor: reduceTaskEditor,
  practice: reducePractice,
  intl: intlReducer,
  routing: routerReducer,
});


export default reducers;
