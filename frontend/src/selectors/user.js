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
    isStaff: user.isStaff,
    created: user.created,
    initial: getInitial(user),
  };
}


function getInitial(user) {
  if (user.isLazy) {
    return 'a'
  };
  const name = user.nickname || user.email || 'A';
  const letter = name[0];
  return letter.toUpperCase();
}
