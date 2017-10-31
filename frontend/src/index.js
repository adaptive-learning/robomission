import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter } from 'react-router-dom';
import AppContainer from './containers/AppContainer';
import HomePage from './pages/HomePage';
//import PracticePage from './pages/PracticePage';
//import TaskEditorPage from './pages/TaskEditorPage';
//import TasksTableContainer from './containers/TasksTableContainer';
//import FlocsProvider from './FlocsProvider';
import { Provider } from 'react-intl-redux';

import { globalConfiguration } from './config';
import { createFlocsStore } from './store';
import FlocsThemeProvider from './theme/FlocsThemeProvider';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
// for testing:
import App from './App';

globalConfiguration();

const store = createFlocsStore();

//const routes = (
//  <Route path="/" component={AppContainer}>
//    <IndexRoute component={HomePage} />
//  </Route>
//);
// TODO: add following routes:
//    <Route path="/tasks" component={TasksTableContainer} />
//    <Route path="/task/:taskId" component={PracticePage} />
//    <Route path="/task-editor" component={TaskEditorPage} />

//const app = (
//  <FlocsProvider store={store} router>
//    {routes}
//  </FlocsProvider>
//);
const app = (
  <Provider store={store}>
    <FlocsThemeProvider>
      <BrowserRouter>
        <AppContainer />
      </BrowserRouter>
    </FlocsThemeProvider>
  </Provider>
);

const mountElement = document.getElementById('flocsApp');
ReactDOM.render(app, mountElement);
registerServiceWorker();
