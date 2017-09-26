import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { FormattedMessage } from 'react-intl';


export default class TaskFailedModal extends React.Component {
  render() {
    const actions = [
      <FlatButton
        label="Reset"
        secondary={true}
        keyboardFocused={true}
        onTouchTap={this.props.resetGame}
      />,
    ];
    return (
      <Dialog
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.resetGame}
        overlayStyle={{ backgroundColor: 'transparent' }}
        contentStyle={{ width: 500 }}
      >
        <FormattedMessage id={`fail-reason.${this.props.reason}`} />
      </Dialog>
    );
  }
}
