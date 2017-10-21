import { combineReducers } from 'redux';
import * as actionType from '../actions/types';

const worldInitialState = null;
const reduceWorld = (state = worldInitialState, action) => {
  switch(action.type) {
    case actionType.FETCH_WORLD_FULFILLED:
      return action.data;
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  world: reduceWorld,
});

export default rootReducer;
