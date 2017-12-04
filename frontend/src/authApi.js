/**
 * Defines API for authentication.
 */
import axios from 'axios';


const AUTH_API_PATH = '/rest-auth/';
const FB_APP_ID = '1705808839684479';
const GOOGLE_APP_ID = '398125540084-8866rbhsa81j25das3euqe6ifcd31dgg.apps.googleusercontent.com';


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
  const url = `${AUTH_API_PATH}facebook/`;
  const data = {
    code: FB_APP_ID,
  };
  return axios.post(url, data);
}


export function loginViaGoogle() {
  const url = `${AUTH_API_PATH}google/`;
  const data = {
    code: GOOGLE_APP_ID,
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
