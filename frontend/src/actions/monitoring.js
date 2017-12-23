import * as at from '../action-types';


function action(type, payload = {}) {
  return {type, payload}
}


export const fetchMetrics = {
  request: () => action(at.FETCH_METRICS_REQUEST),
  success: (metrics) => action(at.FETCH_METRICS_SUCCESS, {metrics}),
  failure: (error) => action(at.FETCH_METRICS_FAILURE, {error}),
}
