import React from 'react';
import { Redirect, Route, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { getUser } from '../selectors/user';


const getProps = state => ({
  user: getUser(state),
});


class PrivateRoute extends React.Component {
  render() {
    const { user, component: Component, ...rest } = this.props;
    const renderComponentOrRedirect = (props) => {
      if (user.isStaff) {
        return (
          <Component {...props}/>
        );
      }
      if (!user.isLazy) {
        return (
          <div style={{ color: 'white', margin: 10 }}>
            <p>
              This page is only for staff members.
              Logout from the current account and login to a staff member
              account. Or ask an admin to give you the needed permissions.
            </p>
          </div>
        );
      }
      return (
        <Redirect to={{
          pathname: '/login',
          state: { from: props.location, requireStaffUser: true }
        }}/>
      );
    }
    return (
      <Route {...rest} render={renderComponentOrRedirect} />
    );
  }
}


PrivateRoute = withRouter(connect(getProps)(PrivateRoute));
export default PrivateRoute;
