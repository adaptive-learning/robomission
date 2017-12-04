import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import App from '../components/App';
import LoadingIndicator from '../components/LoadingIndicator';
import {
  isLoaded,
  isLoginModalOpen,
  isSignUpModalOpen,
  getLoginFailed,
  getSignUpModalErrors,
  } from '../selectors/app';
import { getProfile, getCredentials } from '../selectors/user';
import {
  changeLocation,
  changeCredentials,
  changeNickname,
  login,
  signUp,
  toggleLoginModal,
  toggleSignUpModal
  } from '../actions';


const propTypes = {
  loaded: PropTypes.bool.isRequired,
  showLoginModal: PropTypes.bool.isRequired,
  loginFailed: PropTypes.bool.isRequired,
  showSignUpModal: PropTypes.bool.isRequired,
  signUpModalErrors: PropTypes.object.isRequired,
  children: PropTypes.node,
};

const defaultProps = {
  loaded: false,
};

const getProps = state => ({
  loaded: isLoaded(state),
  showLoginModal: isLoginModalOpen(state),
  loginFailed: getLoginFailed(state),
  showSignUpModal: isSignUpModalOpen(state),
  signUpModalErrors: getSignUpModalErrors(state),
  credentials: getCredentials(state),
  profile: getProfile(state),
});

const actionCreators = {
  changeLocation,
  toggleLoginModal,
  toggleSignUpModal,
  changeCredentials,
  changeNickname,
  login: login.request,
  signUp: signUp.request,
};

class AppContainer extends React.Component {
  // Previously, global data was fetched on mount of this top-level container,
  // but we have moved this logic into the root saga.
  constructor(props) {
    super(props);
    this.closeLoginModal = this.props.toggleLoginModal.bind(this, false);
    this.closeSignUpModal = this.props.toggleSignUpModal.bind(this, false);
    this.openSignUpModal = this.props.toggleSignUpModal.bind(this, true);
    this.changeCredentials = this.props.changeCredentials.bind(this);
    this.changeProfile = ({ nickname }) => { this.props.changeNickname(nickname); };
    this.login = this.props.login.bind(this);
    this.signUp = this.props.signUp.bind(this);
    this.props.changeLocation(props.location);  // report initial location
    this.props.history.listen((location, action) => {
      this.props.changeLocation(location);
    });
  }

  render() {
    if (!this.props.loaded) {
      return (
        <div
          style={{
            width: '100%',
            display: 'table',
            margin: 0,
            height: '100vh',
            backgroundColor: 'rgb(58, 58, 58)',
          }}
        >
          <LoadingIndicator />;
        </div>
      );
    }
    return (
      <App
        showLoginModal={this.props.showLoginModal}
        loginFailed={this.props.loginFailed}
        showSignUpModal={this.props.showSignUpModal}
        signUpModalErrors={this.props.signUpModalErrors}
        credentials={this.props.credentials}
        profile={this.props.profile}
        changeCredentials={this.changeCredentials}
        changeProfile={this.changeProfile}
        login={this.login}
        signUp={this.signUp}
        closeLoginModal={this.closeLoginModal}
        closeSignUpModal={this.closeSignUpModal}
        openSignUpModal={this.openSignUpModal}
      >
        {this.props.children}
      </App>
    );
  }
}

AppContainer.propTypes = propTypes;
AppContainer.defaultProps = defaultProps;

// AppContainer contains routes, so it needs to rerender on location change,
// which is achieved by `withRouter` wrapper.
// Details: https://reacttraining.com/react-router/web/guides/redux-integration
AppContainer = withRouter(connect(getProps, actionCreators)(AppContainer));

export default AppContainer;
