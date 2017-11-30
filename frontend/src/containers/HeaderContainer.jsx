import React from 'react';
import { connect } from 'react-redux';
import { setOpenMenu, toggleFeedbackModal, toggleLoginModal } from '../actions';
import { getLevelStatus } from '../selectors/student';
import { getUser } from '../selectors/user';
import Header from '../components/Header';


const getProps = state => ({
  levelStatus: getLevelStatus(state),
  user: getUser(state),
});

const actionCreators = {
  setOpenMenu,
  toggleFeedbackModal,
  toggleLoginModal,
};

class HeaderContainer extends React.Component {
  constructor(props) {
    super(props);
    this.openMenu = this.props.setOpenMenu.bind(this, true);
    this.openFeedbackModal = this.props.toggleFeedbackModal.bind(this, true);
    this.openLoginModal = this.props.toggleLoginModal.bind(this, true);
  }

  render(){
    return (
      <Header
        onMenuIconTouchTap={this.openMenu}
        levelInfo={this.props.levelStatus}
        openFeedbackModal={this.openFeedbackModal}
        openLoginModal={this.openLoginModal}
        user={this.props.user}
      />
  )}
}

HeaderContainer = connect(getProps, actionCreators)(HeaderContainer);

export default HeaderContainer;
