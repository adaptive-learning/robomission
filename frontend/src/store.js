import { createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import createSagaMiddleware from 'redux-saga';

import { getLocalizationSetting } from './localization';
import rootReducer from './reducers';
import rootSaga from './sagas';


export function createFlocsStore(initialState) {
  const initialStateWithLocalization = {
    ...initialState,
    intl: getLocalizationSetting(),
  };
  const sagaMiddleware = createSagaMiddleware();
  const loggerMiddleware = createLogger();
  const middleware = applyMiddleware(sagaMiddleware, loggerMiddleware);
  const store = createStore(rootReducer, initialStateWithLocalization, middleware);
  // TODO: Rewrite all sagas without need for dispatch and getState;
  //       then remove these two parameters.
  sagaMiddleware.run(rootSaga, store.dispatch, store.getState);
  return store;
}
