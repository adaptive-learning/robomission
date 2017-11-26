import React from 'react';
import Drawer from 'material-ui/Drawer';
import { Menu as MaterialMenu } from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import muiThemeable from 'material-ui/styles/muiThemeable';
import HomeIcon from 'material-ui/svg-icons/action/home';
import TaskIcon from 'material-ui/svg-icons/av/play-arrow';
import TasksOverviewIcon from 'material-ui/svg-icons/image/view-comfy';
import TaskEditorIcon from 'material-ui/svg-icons/action/note-add';
import FeedbackIcon from 'material-ui/svg-icons/action/feedback';
import { Link } from 'react-router-dom';
import Text from '../localization/Text';



class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.setOpen = this.props.setOpen.bind(this);
    this.openFeedbackModal = this.props.openFeedbackModal.bind(this);
  }

  render() {
    let practiceTaskUrl = '';
    if (this.props.recommendedTask !== null) {
      practiceTaskUrl = this.props.recommendedTask.url;
    }
    return (
      <Drawer
        docked={false}
        open={this.props.open}
        onRequestChange={this.setOpen}
      >
        {/*
        <MenuItem>Log in</MenuItem>
        <MenuItem>Sign up</MenuItem>
        <Divider />
        */}
        <MaterialMenu
          value={this.props.mode}
          autoWidth={false}
          width={this.props.muiTheme.drawer.width}
          disableAutoFocus={true}
        >
        { /* Note that disabling auto focus on menu is important to avoid
        material-ui bug of menu steeling focus to text fields when typing, see
        https://github.com/callemall/material-ui/issues/4387 */ }
          <MenuItem
            value="intro"
            leftIcon={<HomeIcon />}
            containerElement={<Link to="/" />}
          >
            <Text id="Intro" />
          </MenuItem>
          <MenuItem
            value="task"
            leftIcon={<TaskIcon />}
            containerElement={<Link to={practiceTaskUrl} />}
          >
            <Text id="Practice" />
          </MenuItem>
          <MenuItem
            value="tasks"
            leftIcon={<TasksOverviewIcon />}
            containerElement={<Link to="/tasks" />}
          >
            <Text id="Tasks" />
          </MenuItem>
          <Divider />
          <Subheader>Pro hackery</Subheader>
          <MenuItem
            value="task-editor"
            leftIcon={<TaskEditorIcon />}
            containerElement={<Link to="/task-editor" />}
          >
            <Text id="Task Editor" />
          </MenuItem>
          <Divider />
          <MenuItem
            value="feedback"
            leftIcon={<FeedbackIcon />}
            onClick={this.openFeedbackModal}
          >
            <Text id="Feedback" />
          </MenuItem>
        </MaterialMenu>
      </Drawer>
    );
  }
}

Menu = muiThemeable()(Menu);

export default Menu;
