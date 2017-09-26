import ReactGA from 'react-ga';
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import createPromiseMiddleware from 'redux-promise-middleware';
import createLoggerMiddleware from 'redux-logger';
import axiosDefaults from 'axios/lib/defaults';
import rootReducer from './reducers';
import { getLocalizationSetting } from './localization';
import { initGlobalBlockly } from './core/blockly';
import { initGlobalTheme } from './theme';


export function globalConfiguration() {
  initGoogleAnalytics();
  initGlobalAxios();
  initGlobalTheme();
  initGlobalBlockly();
}


function initGoogleAnalytics() {
  const trackingId = 'UA-81667720-1';
  ReactGA.initialize(trackingId, { debug: false, titleCase: false });
}


function initGlobalAxios() {
  axiosDefaults.xsrfCookieName = 'csrftoken';
  axiosDefaults.xsrfHeaderName = 'X-CSRFToken';
}


export function configureStore(initialState) {
  const initialStateWithLocalization = {
    ...initialState,
    intl: getLocalizationSetting(),
  };
  const promise = createPromiseMiddleware();
  const logger = createLoggerMiddleware();
  const middleware = applyMiddleware(promise, thunk, logger);
  const store = createStore(rootReducer, initialStateWithLocalization, middleware);

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('./reducers', () => {
      const nextRootReducer = require('./reducers/index').reducers;
      store.replaceReducer(nextRootReducer);
    });
  }

  return store;
}
