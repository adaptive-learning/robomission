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
import EyeIcon from 'material-ui/svg-icons/image/remove-red-eye';
import DBIcon from 'material-ui/svg-icons/device/storage';
import { Link } from 'react-router-dom';
import GHIcon from '../components/GitHubIcon';
import Text from '../localization/Text';
//import logoMenuPath from '../images/logo-menu.png';
import Image from'../components/Image';


class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.setOpen = this.props.setOpen.bind(this);
    this.openFeedbackModal = this.props.openFeedbackModal.bind(this);
  }

  renderAdminMenu() {
    if (!this.props.user.isStaff) {
      return null;
    }
    return [
      (<Divider key="divivider-admin" />),
      (<Subheader key="subheader-admin" >Admin</Subheader>),
      (
        <MenuItem
          value="admin"
          key="admin"
          leftIcon={<DBIcon />}
          href="/admin/"
          target="_blank"
          rel="noreferrer noopener"
        >
          DB Admin
        </MenuItem>
      ), (
        <MenuItem
          value="monitoring"
          key="monitoring"
          leftIcon={<EyeIcon />}
          containerElement={<Link to="/monitoring" />}
        >
          Monitoring
        </MenuItem>
      ), (
        <MenuItem
          value="github"
          key="github"
          leftIcon={<GHIcon />}
          href="https://github.com/adaptive-learning/robomission"
          target="_blank"
          rel="noreferrer noopener"
        >
          Repo
        </MenuItem>
      ),
    ];
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
        <Image imageId="menu-banner" style={{ width: "100%", marginBottom: -12 }} />
        <MaterialMenu
          value={this.props.mode}
          autoWidth={false}
          width={this.props.muiTheme.drawer.width}
          disableAutoFocus={true}
        >
        { /* Note that disabling auto focus on menu is important to avoid
        material-ui bug of menu steeling focus to text fields when typing, see
        https://github.com/callemall/material-ui/issues/4387 */ }
          <Divider style={{ marginTop: 0 }} />
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
          <MenuItem
            value="task-editor"
            leftIcon={<TaskEditorIcon />}
            containerElement={<Link to="/task-editor" />}
          >
            <Text id="Task Editor" />
          </MenuItem>
          <MenuItem
            value="feedback"
            leftIcon={<FeedbackIcon />}
            onClick={this.openFeedbackModal}
          >
            <Text id="Feedback" />
          </MenuItem>
          {this.renderAdminMenu()}
        </MaterialMenu>
      </Drawer>
    );
  }
}

Menu = muiThemeable()(Menu);

export default Menu;
