import { LOCATION_CHANGE } from 'react-router-redux';

const initialState = {
  open: false,
};

export default function reduceMenu(state = initialState, action) {
  switch (action.type) {
    case 'MENU.SET_OPEN':
      return {
        ...state,
        open: action.payload.open,
      };
    case LOCATION_CHANGE:
      return {
        ...state,
        open: false,
      };
  }
  return state;
}
