export function isFeedbackModalOpen(state) {
  return state.feedback.open;
}

export function getFeedback(state) {
  const { comment, email } = state.feedback;
  return { comment, email };
}
