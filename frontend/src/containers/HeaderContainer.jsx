import React from 'react';
import { connect } from 'react-redux';
import {
  setOpenMenu,
  showInstructions,
  toggleFeedbackModal,
  toggleLoginModal,
  toggleSignUpModal,
  logout } from '../actions';
import { getNNewInstructions } from '../selectors/instructions';
import { getLevelStatus } from '../selectors/student';
import { getUser } from '../selectors/user';
import { getMode } from '../selectors/app';
import Header from '../components/Header';


const getProps = state => ({
  levelStatus: getLevelStatus(state),
  nNewInstructions: getNNewInstructions(state),
  user: getUser(state),
  mode: getMode(state),
});

const actionCreators = {
  showInstructions,
  setOpenMenu,
  toggleFeedbackModal,
  toggleLoginModal,
  toggleSignUpModal,
  logout: logout.request,
};

class HeaderContainer extends React.Component {
  constructor(props) {
    super(props);
    this.showInstructions = this.props.showInstructions.bind(this);
    this.openMenu = this.props.setOpenMenu.bind(this, true);
    this.openFeedbackModal = this.props.toggleFeedbackModal.bind(this, true);
    this.openLoginModal = this.props.toggleLoginModal.bind(this, true);
    this.openSignUpModal = this.props.toggleSignUpModal.bind(this, true);
    this.logout = this.props.logout.bind(this);
  }

  render() {
    return (
      <Header
        onMenuIconTouchTap={this.openMenu}
        levelInfo={this.props.levelStatus}
        nNewInstructions={this.props.nNewInstructions}
        showInstructions={this.showInstructions}
        openFeedbackModal={this.openFeedbackModal}
        openLoginModal={this.openLoginModal}
        openSignUpModal={this.openSignUpModal}
        logout={this.logout}
        user={this.props.user}
        mode={this.props.mode}
      />
  )}
}

HeaderContainer = connect(getProps, actionCreators)(HeaderContainer);

export default HeaderContainer;
