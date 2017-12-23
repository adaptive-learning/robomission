import { FETCH_METRICS_SUCCESS } from '../action-types';


const initialState = {
  metrics: null,
};


export default function reduceMonitoring(state = initialState, action) {
  switch (action.type) {
    case FETCH_METRICS_SUCCESS: {
      return {
        ...state,
        ...action.payload,
      };
    }
    default: {
      return state;
    }
  }
}
