import { TOGGLE_FEEDBACK_MODAL,
         CHANGE_FEEDBACK,
         SUBMIT_FEEDBACK_SUCCESS } from '../action-types';

const initialState = {
  open: false,
  comment: '',
  email: '',
};

export default function reduceMenu(state = initialState, action) {
  switch (action.type) {
    case TOGGLE_FEEDBACK_MODAL:
      return {
        ...state,
        open: action.payload.open,
      };
    case CHANGE_FEEDBACK:
      return {
        ...state,
        ...action.payload.feedback,
      };
    case SUBMIT_FEEDBACK_SUCCESS:
      return {
        ...state,
        comment: '',
      };
    default: {
      return state;
    }
  }
}
