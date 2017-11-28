import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import App from '../components/App';
import LoadingIndicator from '../components/LoadingIndicator';
import { isLoaded, isLoginModalOpen } from '../selectors/app';
import { getCredentials } from '../selectors/user';
import { changeLocation, changeCredentials, login, toggleLoginModal } from '../actions';


const propTypes = {
  loaded: PropTypes.bool.isRequired,
  showLoginModal: PropTypes.bool.isRequired,
  children: PropTypes.node,
};

const defaultProps = {
  loaded: false,
};

const getProps = state => ({
  loaded: isLoaded(state),
  showLoginModal: isLoginModalOpen(state),
  credentials: getCredentials(state),
});

const actionCreators = {
  changeLocation,
  toggleLoginModal,
  changeCredentials,
  login: login.request,
};

class AppContainer extends React.Component {
  // Previously, global data was fetched on mount of this top-level container,
  // but we have moved this logic into the root saga.
  constructor(props) {
    super(props);
    this.closeLoginModal = this.props.toggleLoginModal.bind(this, false);
    this.changeCredentials = this.props.changeCredentials.bind(this);
    this.login = this.props.login.bind(this);
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
        credentials={this.props.credentials}
        changeCredentials={this.changeCredentials}
        login={this.login}
        closeLoginModal={this.closeLoginModal}
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
