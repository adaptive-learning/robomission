import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import EmailIcon from 'material-ui/svg-icons/communication/email';
import { translate } from '../localization';


export default class LoginModal extends React.Component {
  render() {
    const changeEmail = (event) => {
      const credentials = {...this.props.credentials, email: event.target.value};
      this.props.changeCredentials(credentials);
    }
    const changePassword = (event) => {
      const credentials = {...this.props.credentials, password: event.target.value};
      this.props.changeCredentials(credentials);
    }
    const login = () => {
      this.props.login(this.props.credentials);
    };
    const actions = [
      <FlatButton
        label={translate('user.login')}
        primary={true}
        onClick={login}
      />,
    ];
    return (
      <Dialog
        title={translate('user.login')}
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.closeLoginModal}
        contentStyle={{ width: 500 }}
      >
        <TextField
          id='login-email'
          floatingLabelText={translate('user.email')}
          value={this.props.credentials.email}
          onChange={changeEmail}
          fullWidth={true}
          type="email"
        />
        <TextField
          id='login-password'
          floatingLabelText={translate('user.password')}
          value={this.props.credentials.password}
          onChange={changePassword}
          fullWidth={true}
          type="password"
        />
        <RaisedButton
          label={translate('user.signup')}
          primary={true}
          onClick={this.props.openSignUpModal}
          icon={<EmailIcon />}
        />
      </Dialog>
    );
  }
}
