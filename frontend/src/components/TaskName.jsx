import React from 'react';
import PropTypes from 'prop-types';
import { toTitle } from '../utils/text';
import { possiblyTranslate } from '../localization';

export default function TaskName({ taskId }) {
  return (
    <span>{getLocalizedTaskName(taskId)}</span>
  );
}


TaskName.propTypes = {
  taskId: PropTypes.string.isRequired,
};


function getLocalizedTaskName(taskId) {
  if (!taskId) {
    return '';
  }
  const fallback = toTitle(taskId);
  return possiblyTranslate(`task.${taskId}`, fallback);
}
