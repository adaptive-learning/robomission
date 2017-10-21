import { compose, createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import createSagaMiddleware from 'redux-saga';

import rootReducer from './reducers';
import rootSaga from './sagas';


const sagaMiddleware = createSagaMiddleware();
const loggerMiddleware = createLogger();
const middleware = applyMiddleware(sagaMiddleware, loggerMiddleware);
const store = createStore(rootReducer, middleware);

sagaMiddleware.run(rootSaga);

export default store;
