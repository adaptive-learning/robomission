import * as at from '../action-types';

function action(type, payload = {}) {
  return {type, payload}
}


export const fetchWorld = {
  //request: login => action(at.FETCH_WORLD_REQUEST),
  success: (world) => action(at.FETCH_WORLD_SUCCESS, world),
  failure: (error) => action(at.FETCH_WORLD_FAILURE, {error}),
}


export const fetchUser = {
  request: login => action(at.FETCH_USER_REQUEST),
  success: (user) => action(at.FETCH_USER_SUCCESS, user),
  failure: (error) => action(at.FETCH_USER_FAILURE, {error}),
}
