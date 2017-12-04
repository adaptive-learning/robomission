import React from 'react';
import PropTypes from 'prop-types';
import Snackbar from 'material-ui/Snackbar';
import backgroundPath from '../images/background-space.png';
import HeaderContainer from '../containers/HeaderContainer';
import MenuContainer from '../containers/MenuContainer';
import InstructionsContainer from '../containers/InstructionsContainer';
import FeedbackModalContainer  from '../containers/FeedbackModalContainer';
import LoginModal from '../components/LoginModal';
import SignUpModal from '../components/SignUpModal';
import { translate } from '../localization';


const propTypes = {
  children: PropTypes.node,
  showLoginModal: PropTypes.bool.isRequired,
  openSignUpModal: PropTypes.func.isRequired,
};

export default class App extends React.Component {
  render() {
    return (
      <div
        style={{
          backgroundImage: `url(${backgroundPath})`,
          backgroundSize: '500px auto',
          backgroundColor: '#111122',
          paddingBottom: 25,
          overflowX: 'hidden',
        }}
      >
        <InstructionsContainer />
        <HeaderContainer />
        <MenuContainer />
        { this.props.children }
        <FeedbackModalContainer />
        <LoginModal
          open={this.props.showLoginModal}
          credentials={this.props.credentials}
          loginFailed={this.props.loginFailed}
          changeCredentials={this.props.changeCredentials}
          closeLoginModal={this.props.closeLoginModal}
          openSignUpModal={this.props.openSignUpModal}
          login={this.props.login}
        />
        <SignUpModal
          open={this.props.showSignUpModal}
          credentials={this.props.credentials}
          profile={this.props.profile}
          fieldErrors={this.props.signUpModalErrors}
          changeCredentials={this.props.changeCredentials}
          changeProfile={this.props.changeProfile}
          closeSignUpModal={this.props.closeSignUpModal}
          signup={this.props.signUp}
        />
        <Snackbar
          open={this.props.snackbarMessageId !== null}
          message={this.props.snackbarMessageId ? translate(this.props.snackbarMessageId) : ''}
          autoHideDuration={4000}
        />
      </div>
    );
  }
}


App.propTypes = propTypes;
