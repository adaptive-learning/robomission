import React from 'react';
import { Redirect, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { toggleLoginModal } from '../actions';
import { getUser } from '../selectors/user';
import LongPage from '../components/LongPage';


const getProps = state => ({
  user: getUser(state),
});

const actionCreators = {
  toggleLoginModal,
};


class LoginPage extends React.Component {
  componentDidMount() {
    if (this.props.user.isLazy) {
      this.props.toggleLoginModal(true);
    }
  }

  // Login page is just empty page with login modal open.
  // TODO: Make it look better - plain page with login content, but not inside a modal.
  render() {
    const { user } = this.props;
    const { from } = this.props.location.state || { from: { pathname: '/' } };
    if (user.isLazy) {
      return (
        <LongPage />
      );
    }
    return (
      <Redirect to={from}/>
    );
  }
}


LoginPage = withRouter(connect(getProps, actionCreators)(LoginPage));
export default LoginPage;
