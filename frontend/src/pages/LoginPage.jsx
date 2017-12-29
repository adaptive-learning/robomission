import React from 'react';
import { Redirect, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { toggleLoginModal } from '../actions';
import { getUser } from '../selectors/user';


const getProps = state => ({
  user: getUser(state),
});

const actionCreators = {
  toggleLoginModal,
};


// TODO: factor out longPageStyle (used in other pages as well)
const longPageContentStyle = {
  maxWidth: 1200,
  margin: '20px auto',
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
        <div style={longPageContentStyle} />
      );
    }
    return (
      <Redirect to={from}/>
    );
  }
}


LoginPage = withRouter(connect(getProps, actionCreators)(LoginPage));
export default LoginPage;
