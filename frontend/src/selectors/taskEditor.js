export function isVimModeEnabled(state) {
  const editor = getTaskEditor(state);
  return editor.vimMode;
}


export function getTaskEditor(state) {
  return state.taskEditor;
}

