import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import NextTaskButton from '../components/NextTaskButton';
import { getRecommendedTask } from '../selectors/practice';

function getProps(state) {
  const task = getRecommendedTask(state);
  return { task };
}

class NextTaskButtonContainer extends React.Component {
  render() {
    return (
      <NextTaskButton task={this.props.task} />
    );
  }
}

NextTaskButtonContainer.propTypes = {
  task: PropTypes.object,
};

NextTaskButtonContainer = connect(getProps)(NextTaskButtonContainer);

export default NextTaskButtonContainer;
