export function getCredentials(state) {
  return state.user.credentials;
}

export function getProfile(state) {
  return { nickname: state.user.nickname };
}
