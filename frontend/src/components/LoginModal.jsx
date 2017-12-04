import React from 'react';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import {GridList, GridTile} from 'material-ui/GridList';
import TextField from 'material-ui/TextField';
import EmailIcon from 'material-ui/svg-icons/communication/email';
import { FacebookLoginButton, GoogleLoginButton } from 'react-social-login-buttons';
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
      this.props.login({ credentials: this.props.credentials });
    };
    const loginViaFacebook = () => {
      this.props.login({ provider: 'facebook' });
    };
    const loginViaGoogle = () => {
      this.props.login({ provider: 'google' });
    };
    const buttonStyle = {
      boxShadow: 'none',
      margin: 0,
      marginBottom: 10,
      height: 50,
    };
    return (
      <Dialog
        title={translate('user.login')}
        open={this.props.open}
        onRequestClose={this.props.closeLoginModal}
        contentStyle={{ width: 540 }}
      >
        <GridList
          cellHeight="auto"
          cols={2}
          padding={20}
        >
          <GridTile>
            <GoogleLoginButton
              text={translate('user.via-google')}
              style={buttonStyle}
              onClick={loginViaGoogle}
            />
            <FacebookLoginButton
              text={translate('user.via-facebook')}
              style={buttonStyle}
              onClick={loginViaFacebook}
            />
            <RaisedButton
              label={translate('user.signup')}
              primary={true}
              style={{ height: 50 }}
              buttonStyle={{ textAlign: 'left' }}
              fullWidth={true}
              onClick={this.props.openSignUpModal}
              icon={<EmailIcon />}
            />
          </GridTile>
          <GridTile>
            <TextField
              id='login-email'
              floatingLabelText={translate('user.email')}
              value={this.props.credentials.email}
              onChange={changeEmail}
              fullWidth={true}
              type="email"
              style={{ marginTop: -20 }}
            />
            <TextField
              id='login-password'
              floatingLabelText={translate('user.password')}
              value={this.props.credentials.password}
              onChange={changePassword}
              fullWidth={true}
              type="password"
              errorText={this.props.loginFailed ? translate('user.login-failed') : null}
            />
            <RaisedButton
              label={translate('user.login')}
              primary={true}
              onClick={login}
              fullWidth={true}
              style={{ marginTop: 10 }}
            />
          </GridTile>
        </GridList>
      </Dialog>
    );
  }
}
