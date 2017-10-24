import * as at from '../action-types';


function action(type, payload = {}) {
  return {type, payload}
}


export const fetchApiRoot = {
  //request: () => action(at.FETCH_API_ROOT_REQUEST),
  success: (apiRoot) => action(at.FETCH_API_ROOT_SUCCESS, apiRoot),
  failure: (error) => action(at.FETCH_API_ROOT_FAILURE, {error}),
}


export const fetchWorld = {
  //request: () => action(at.FETCH_WORLD_REQUEST),
  success: (world) => action(at.FETCH_WORLD_SUCCESS, world),
  failure: (error) => action(at.FETCH_WORLD_FAILURE, {error}),
}


export const fetchUser = {
  request: (url) => action(at.FETCH_USER_REQUEST, {url}),
  success: (user) => action(at.FETCH_USER_SUCCESS, user),
  failure: (error) => action(at.FETCH_USER_FAILURE, {error}),
}


export const fetchStudent = {
  request: (url) => action(at.FETCH_STUDENT_REQUEST, {url}),
  success: (student) => action(at.FETCH_STUDENT_SUCCESS, student),
  failure: (error) => action(at.FETCH_STUDENT_FAILURE, {error}),
}


export const fetchPracticeOverview = {
  request: (url) => action(at.FETCH_PRACTICE_OVERVIEW_REQUEST, {url}),
  success: (practiceOverivew) => action(at.FETCH_PRACTICE_OVERVIEW_SUCCESS, practiceOverivew),
  failure: (error) => action(at.FETCH_PRACTICE_OVERVIEW_FAILURE, {error}),
}
