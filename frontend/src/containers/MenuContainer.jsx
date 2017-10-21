import React from 'react';
import { connect } from 'react-redux';
import { setOpenMenu } from '../actions/menu';
import Menu from '../components/Menu';
import { getRecommendedTask } from '../selectors/practice';
import { getMode } from '../selectors/app';


@connect(state => ({
  mode: getMode(state),
  open: state.menu.open,
  recommendedTask: getRecommendedTask(state)
}), {
  setOpenMenu
})
class MenuContainer extends React.Component {
  constructor(props) {
    super(props);
    this.setOpen = this.props.setOpenMenu.bind(this);
  }

  render(){
    return (
      <Menu
        mode={this.props.mode}
        open={this.props.open}
        setOpen={this.setOpen}
        recommendedTask={this.props.recommendedTask}
      />
  )}
}

export default MenuContainer;
