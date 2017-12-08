export function isFeedbackModalOpen(state) {
  return state.feedback.open;
}

export function getFeedback(state) {
  const { comment, email } = state.feedback;
  return { comment, email };
}


export function getFeedbackFieldErrors(state) {
  return state.feedback.fieldErrors;
}


export function getIfJustSent(state) {
  return state.feedback.justSent;
}
