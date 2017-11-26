import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { FormattedMessage } from 'react-intl';


export default class FeedbackModal extends React.Component {
  render() {
    const actions = [
      <FlatButton
        label="Reset"
        secondary={true}
        keyboardFocused={true}
        onClick={this.props.resetGame}
      />,
     <FlatButton
        label="Cancel"
        primary={true}
        onClick={this.props.closeFeedbackModal}
      />,
      <FlatButton
        label="Submit"
        primary={true}
        onClick={this.props.submitFeedback}
      />,
    ];
    return (
      <Dialog
        title="Dialog With Actions"
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.closeFeedbackModal}
        overlayStyle={{ backgroundColor: 'transparent' }}
        contentStyle={{ width: 500 }}
      >
        tba: inner text
      </Dialog>
    );
  }
}
