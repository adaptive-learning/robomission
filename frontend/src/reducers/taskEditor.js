import { SWITCH_VIM_MODE } from '../action-types';

const initialState = {
  vimMode: false,
};

export default function reduceTaskEditor(state = initialState, action) {
  switch (action.type) {
    case SWITCH_VIM_MODE:
      return { ...state, vimMode: !state.vimMode };
    default:
      return state;
  }
}
