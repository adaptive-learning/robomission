import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import { translate } from '../localization';


export default class SignUpModal extends React.Component {
  render() {
    const changeEmail = (event) => {
      const credentials = {...this.props.credentials, email: event.target.value};
      this.props.changeCredentials(credentials);
    }
    const changePassword = (event) => {
      const credentials = {...this.props.credentials, password: event.target.value};
      this.props.changeCredentials(credentials);
    }
    const changeNickname = (event) => {
      this.props.changeProfile({ nickname: event.target.value });
    }
    const signup = () => {
      this.props.signup(this.props.profile, this.props.credentials);
    };
    const actions = [
      <FlatButton
        label={translate('user.signup')}
        primary={true}
        onClick={signup}
      />,
    ];
    return (
      <Dialog
        title={translate('user.signup')}
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.closeSignUpModal}
        contentStyle={{ width: 500 }}
      >
        <TextField
          id='signup-email'
          floatingLabelText={translate('user.email')}
          value={this.props.credentials.email}
          onChange={changeEmail}
          fullWidth={true}
          type="email"
          errorText={this.props.fieldErrors.email}
        />
        <TextField
          id='signup-nickname'
          floatingLabelText={translate('user.nickname')}
          value={this.props.profile.nickname}
          onChange={changeNickname}
          fullWidth={true}
        />
        <TextField
          id='signup-password'
          floatingLabelText={translate('user.password')}
          value={this.props.credentials.password}
          onChange={changePassword}
          fullWidth={true}
          type="password"
          errorText={this.props.fieldErrors.password}
        />
      </Dialog>
    );
  }
}
