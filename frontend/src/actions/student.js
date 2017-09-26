import axios from 'axios';
import { SET_STUDENT } from '../action-types';


export function getOrCreateStudent() {
  return ((dispatch) => {
    return axios.post('/api/practice/get_or_create_student')
      .then((response) => axios.get(response.data['student_url']))
      .then((response) => dispatch(setStudent(response.data)))
  });
}


export function setStudent(student) {
  return {
    type: SET_STUDENT,
    payload: student,
  };
}
