import React from 'react';
import Drawer from 'material-ui/Drawer';
import { Menu as MaterialMenu } from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import muiThemeable from 'material-ui/styles/muiThemeable';
import { Link } from 'react-router';
import Text from '../localization/Text';


@muiThemeable()
export default class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.setOpen = this.props.setOpen.bind(this);
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
            containerElement={<Link to="/" />}
          >
            <Text id="Intro" />
          </MenuItem>
          <MenuItem
            value="task"
            containerElement={<Link to={practiceTaskUrl} />}
          >
            <Text id="Practice" />
          </MenuItem>
          <MenuItem
            value="tasks"
            containerElement={<Link to="/tasks" />}
          >
            <Text id="Tasks" />
          </MenuItem>
          <Divider />
          <Subheader>Pro hackery</Subheader>
          <MenuItem
            value="task-editor"
            containerElement={<Link to="/task-editor" />}
          >
            <Text id="Task Editor" />
          </MenuItem>
        </MaterialMenu>
      </Drawer>
    );
  }
}
