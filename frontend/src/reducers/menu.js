import { CHANGE_LOCATION, TOGGLE_MENU } from '../action-types';

const initialState = {
  open: false,
};

export default function reduceMenu(state = initialState, action) {
  switch (action.type) {
    case TOGGLE_MENU:
      return {
        ...state,
        open: action.payload.open,
      };
    case CHANGE_LOCATION:
      return {
        ...state,
        open: false,
      };
    default: {
      return state;
    }
  }
}
