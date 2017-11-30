export function getCredentials(state) {
  return state.user.credentials;
}

export function getProfile(state) {
  return { nickname: state.user.nickname };
}

export function getUser(state) {
  const user = state.user;
  return {
    isLazy: user.isLazy,
    initial: getInitial(user),
  };
}


function getInitial(user) {
  if (user.isLazy) {
    return 'a'
  };
  const name = (user.nickname.length > 0) ? user.nickname : user.email;
  const letter = name[0];
  return letter.toUpperCase();
}
