/**
 * Defines API for authentication.
 */
import axios from 'axios';


const AUTH_API_PATH = '/rest-auth/';


export function login(email, password) {
  const url = `${AUTH_API_PATH}login/`;
  const data = {
    username: email,
    email,
    password,
  };
  return axios.post(url, data);
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
  }));
}
