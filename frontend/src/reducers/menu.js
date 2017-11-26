import { CHANGE_LOCATION, TOGGLE_MENU, TOGGLE_FEEDBACK_MODAL } from '../action-types';

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
    case TOGGLE_FEEDBACK_MODAL:
      return {
        ...state,
        open: false,
      };
    default: {
      return state;
    }
  }
}
