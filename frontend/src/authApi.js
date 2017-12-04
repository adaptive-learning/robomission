/**
 * Defines API for authentication.
 */
import axios from 'axios';


const AUTH_API_PATH = '/rest-auth/';


export function login({ email, password }) {
  const url = `${AUTH_API_PATH}login/`;
  const data = {
    username: email,
    email,
    password,
  };
  return axios.post(url, data);
}


export function loginViaFacebook() {
  const path = window.location.pathname;
  const facebookLoginUrl = `/accounts/facebook/login?next=${path}`
  window.location = facebookLoginUrl;
}


export function loginViaGoogle() {
  const path = window.location.pathname;
  const googleLoginUrl = `/accounts/google/login?next=${path}`
  window.location = googleLoginUrl;
}


export function logout() {
  const url = `${AUTH_API_PATH}logout/`;
  return axios.post(url);
}


export function signUp({ email, password }) {
  const url = `${AUTH_API_PATH}registration/`;
  const data = {
    username: email,
    email: email,
    password1: password,
    password2: password,
  };
  return axios.post(url, data).then(response => ({
    token: response.data['key'],
  })).catch(error => {
    const { data } = error.response;
    error.fieldErrors = {
      email: (data.email) ? data.email[0] : null,
      password: (data.password1) ? data.password1[0] : null,
    };
    throw error;
  });
}


export function updateProfile({ nickname }) {
  const url = `${AUTH_API_PATH}user/`;
  const data = {
    first_name: nickname,
  };
  return axios.patch(url, data);
}
