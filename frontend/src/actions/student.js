import { SET_STUDENT } from '../action-types';


export function setStudent(student) {
  return {
    type: SET_STUDENT,
    payload: student,
  };
}
