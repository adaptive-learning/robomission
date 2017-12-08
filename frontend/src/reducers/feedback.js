import {
  TOGGLE_FEEDBACK_MODAL,
  CHANGE_FEEDBACK,
  SUBMIT_FEEDBACK_SUCCESS,
  SUBMIT_FEEDBACK_FAILURE,
  } from '../action-types';

const emptyFieldErrors = {
  comment: null,
  email: null,
};

const initialState = {
  open: false,
  comment: '',
  email: '',
  fieldErrors: emptyFieldErrors,
  justSent: false,
};

export default function reduceMenu(state = initialState, action) {
  switch (action.type) {
    case TOGGLE_FEEDBACK_MODAL:
      return {
        ...state,
        justSent: false,
        open: action.payload.open,
      };
    case CHANGE_FEEDBACK:
      return {
        ...state,
        ...action.payload.feedback,
        fieldErrors: emptyFieldErrors,
      };
    case SUBMIT_FEEDBACK_SUCCESS:
      return {
        ...state,
        comment: '',
        justSent: true,
        fieldErrors: emptyFieldErrors,
      };
    case SUBMIT_FEEDBACK_FAILURE:
      return {
        ...state,
        fieldErrors: action.payload.fieldErrors,
      };
    default: {
      return state;
    }
  }
}
