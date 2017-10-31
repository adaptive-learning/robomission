import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import App from '../components/App';
import LoadingIndicator from '../components/LoadingIndicator';
import { isLoaded } from '../selectors/app';


const propTypes = {
  loaded: PropTypes.bool.isRequired,
  children: PropTypes.node,
  startSession: PropTypes.func,
};

const defaultProps = {
  loaded: false,
};

const getProps = state => ({
  loaded: isLoaded(state),
});

const actionCreators = {};

class AppContainer extends React.Component {
  // Previusly, global data was fetched on mount of this top-level container,
  // but we have moved this logic into the root saga.

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
      <App>
        { this.props.children }
      </App>
    );
  }
}

AppContainer.propTypes = propTypes;
AppContainer.defaultProps = defaultProps;

AppContainer = connect(getProps, actionCreators)(AppContainer);

export default AppContainer;
