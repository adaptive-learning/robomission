import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Link, Route } from 'react-router-dom';
import AppContainer from './containers/AppContainer';
//import FlocsProvider from './FlocsProvider';
import { Provider } from 'react-intl-redux';

import HomePage from './pages/HomePage';
//import PracticePage from './pages/PracticePage';
import TaskEditorPage from './pages/TaskEditorPage';
import TasksTableContainer from './containers/TasksTableContainer';

import { globalConfiguration } from './config';
import { createFlocsStore } from './store';
import FlocsThemeProvider from './theme/FlocsThemeProvider';
import './index.css';
import registerServiceWorker from './registerServiceWorker';

globalConfiguration();

const store = createFlocsStore();
// store.dispatch(
//     {type: 'SET_TASK',
//       payload: {taskEnvironmentId: 'home-commands', taskId: 'beware-of-asteroid'}
//     });

//const routes = (
//  <Route path="/" component={AppContainer}>
//    <IndexRoute component={HomePage} />
//  </Route>
//);
// TODO: add following routes:
//    <Route path="/tasks" component={TasksTableContainer} />
//    <Route path="/task/:taskId" component={PracticePage} />

//const app = (
//  <FlocsProvider store={store} router>
//    {routes}
//  </FlocsProvider>
//);
const app = (
  <Provider store={store}>
    <FlocsThemeProvider>
      <BrowserRouter>
        <AppContainer>
          <Route exact path='/' component={HomePage}/>
          <Route exact path="/tasks" component={TasksTableContainer} />
          <Route path="/task-editor" component={TaskEditorPage} />
        </AppContainer>
      </BrowserRouter>
    </FlocsThemeProvider>
  </Provider>
);

const mountElement = document.getElementById('flocsApp');
ReactDOM.render(app, mountElement);
registerServiceWorker();
