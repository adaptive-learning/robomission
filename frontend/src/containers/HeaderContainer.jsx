import React from 'react';
import { connect } from 'react-redux';
import { setOpenMenu } from '../actions';
import { getLevelStatus } from '../selectors/student';
import Header from '../components/Header';


const getProps = state => ({
  levelStatus: getLevelStatus(state),
});

const actionCreators = {
  setOpenMenu
};

class HeaderContainer extends React.Component {
  constructor(props) {
    super(props);
    this.openMenu = this.props.setOpenMenu.bind(this, true);
  }

  render(){
    return (
      <Header
        onMenuIconTouchTap={this.openMenu}
        levelInfo={this.props.levelStatus}
      />
  )}
}

HeaderContainer = connect(getProps, actionCreators)(HeaderContainer);

export default HeaderContainer;
