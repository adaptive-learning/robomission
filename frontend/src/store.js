import { compose, createStore, applyMiddleware } from 'redux';
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
  sagaMiddleware.run(rootSaga);
  return store;
}
