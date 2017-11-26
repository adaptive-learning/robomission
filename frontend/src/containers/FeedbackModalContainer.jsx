import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import FeedbackModal from '../components/FeedbackModal';
import { changeFeedback, submitFeedback, toggleFeedbackModal } from '../actions';
import { isFeedbackModalOpen, getFeedback } from '../selectors/feedback';


const propTypes = {
  open: PropTypes.bool.isRequired,
  feedback: PropTypes.object.isRequired,
  changeFeedback: PropTypes.func.isRequired,
  submitFeedback: PropTypes.func.isRequired,
  toggleFeedbackModal: PropTypes.func.isRequired,
};


const getProps = state => ({
  open: isFeedbackModalOpen(state),
  feedback: getFeedback(state),
});

const actionCreators = {
  toggleFeedbackModal,
  changeFeedback,
  submitFeedback: submitFeedback.request,
};

class FeedbackModalContainer extends React.Component {
  constructor(props) {
    super(props);
    this.submitFeedback = this.props.submitFeedback.bind(this);
    this.changeFeedback = this.props.changeFeedback.bind(this);
    this.closeFeedbackModal = this.props.toggleFeedbackModal.bind(this, false);
  }

  render() {
    return (
      <FeedbackModal
        open={this.props.open}
        comment={this.props.feedback.comment}
        email={this.props.feedback.email}
        changeFeedback={this.changeFeedback}
        submitFeedback={this.submitFeedback}
        closeFeedbackModal={this.closeFeedbackModal}
      />
    );
  }
}

FeedbackModalContainer.propTypes = propTypes;
FeedbackModalContainer = connect(getProps, actionCreators)(FeedbackModalContainer);

export default FeedbackModalContainer;
