import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import { translate } from '../localization';


export default class FeedbackModal extends React.Component {
  render() {
    if (this.props.justSent) {
      const actions = [
        <FlatButton
          label={translate('Close')}
          primary={true}
          onClick={this.props.closeFeedbackModal}
        />,
      ];
      return (
        <Dialog
          title={translate('feedback.thanks')}
          open={this.props.open}
          actions={actions}
          onRequestClose={this.props.closeFeedbackModal}
        >
        </Dialog>
      );
    }
    const changeComment = (event) => {
      const feedback = {
        comment: event.target.value,
        email: this.props.email,
      };
      this.props.changeFeedback(feedback);
    }
    const changeEmail = (event) => {
      const feedback = {
        comment: this.props.comment,
        email: event.target.value,
      };
      this.props.changeFeedback(feedback);
    }
    const submitFeedback = () => {
      const feedback = {
        comment: this.props.comment,
        email: this.props.email,
      };
      this.props.submitFeedback(feedback);
    };
    const actions = [
      <FlatButton
        label={translate('feedback.submit')}
        primary={true}
        onClick={submitFeedback}
      />,
    ];
    return (
      <Dialog
        title={translate('feedback.title')}
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.closeFeedbackModal}
        contentStyle={{ width: 500 }}
      >
        <TextField
          id='feedback-comment'
          floatingLabelText={translate('feedback.question')}
          value={this.props.comment}
          onChange={changeComment}
          multiLine={true}
          rows={5}
          fullWidth={true}
          errorText={this.props.fieldErrors.comment}
        />
        <TextField
          id='feedback-email'
          floatingLabelText={translate('feedback.email')}
          value={this.props.email}
          onChange={changeEmail}
          fullWidth={true}
          errorText={this.props.fieldErrors.email}
        />
      </Dialog>
    );
  }
}
