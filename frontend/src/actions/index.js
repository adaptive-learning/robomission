import * as actionType from './types';

export const fetchWorld = () => {
  return {
    type: actionType.FETCH_WORLD_REQUESTED,
  }
}
