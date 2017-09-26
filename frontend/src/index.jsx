import React from 'react';
import ReactDOM from 'react-dom';
import { Route, IndexRoute } from 'react-router';
import AppContainer from './containers/AppContainer';
import HomePage from './pages/HomePage';
import PracticePage from './pages/PracticePage';
import TaskEditorPage from './pages/TaskEditorPage';
import TasksTableContainer from './containers/TasksTableContainer';
import FlocsProvider from './FlocsProvider';
import { globalConfiguration, configureStore } from './config';


globalConfiguration();

const store = configureStore();

const routes = (
  <Route path="/" component={AppContainer}>
    <IndexRoute component={HomePage} />
    <Route path="/tasks" component={TasksTableContainer} />
    <Route path="/task/:taskId" component={PracticePage} />
    <Route path="/task-editor" component={TaskEditorPage} />
  </Route>
);

const app = (
  <FlocsProvider store={store} router>
    {routes}
  </FlocsProvider>
);

const mountElement = document.getElementById('flocsApp');
ReactDOM.render(app, mountElement);
