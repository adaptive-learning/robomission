import React from 'react';
import AppBar from 'material-ui/AppBar';
import Avatar from 'material-ui/Avatar';
import { Toolbar, ToolbarGroup, ToolbarSeparator } from 'material-ui/Toolbar';
import FeedbackIcon from 'material-ui/svg-icons/action/feedback';
import UserIcon from 'material-ui/svg-icons/social/person';
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import muiThemeable from 'material-ui/styles/muiThemeable';
import logo from '../images/logo.png'
import LevelBar from '../components/LevelBar';
import { translate } from '../localization';


class Header extends React.Component {
  renderTitle() {
    const logoImg = (
      <img
        alt='RoboMission logo'
        src={ logo }
        style={{
          height: '100%',
          padding: 14,
          boxSizing: 'border-box',
        }}
      />
    );
    let modeTitleText = '';
    if (this.props.mode === 'monitoring') {
      modeTitleText = 'Monitoring';
    }
    const modeTitle = (
      <span style={{ position: 'absolute', top: 0, marginLeft: 15, color: 'white' }}>
        {modeTitleText}
      </span>
    );
    return [logoImg, modeTitle];
  }
  render() {
    let userIcon = (<UserIcon />);
    if (!this.props.user.isLazy) {
      userIcon = this.props.user.initial;
    }
    const avatar = (
      <IconButton style={{padding: 0}}>
        <Avatar>
          {userIcon}
        </Avatar>
      </IconButton>
    );
    let userMenu = (
      <IconMenu iconButtonElement={avatar}>
        <MenuItem
          primaryText={translate('user.login')}
          onClick={this.props.openLoginModal}
        />
        <MenuItem
          primaryText={translate('user.signup')}
          onClick={this.props.openSignUpModal}
        />
        <MenuItem
          primaryText={translate('user.delete-history')}
          onClick={this.props.logout}
        />
      </IconMenu>
    );
    if (!this.props.user.isLazy) {
      userMenu = (
        <IconMenu iconButtonElement={avatar}>
          <MenuItem
            primaryText={translate('user.logout')}
            onClick={this.props.logout}
          />
        </IconMenu>
      );
    }
    const toolbar = (
      <Toolbar style={{ backgroundColor: 'transparent', color: 'white' }}>
        {this.props.mode !== 'monitoring' && [(
          <ToolbarGroup>
            <LevelBar mini {...this.props.levelInfo} />
          </ToolbarGroup>
        ),
        (
          <ToolbarSeparator
            style={{
              position: 'relative',
              top: 9,
            }}
          />
        )]}
        <ToolbarGroup lastChild={true}>
          <IconButton
            tooltip={translate('Feedback')}
            onClick={this.props.openFeedbackModal}
          >
            <FeedbackIcon />
          </IconButton>
          {userMenu}
        </ToolbarGroup>
      </Toolbar>
    );
    return (
      <AppBar
        title={this.renderTitle()}
        style={{
          backgroundColor: this.props.muiTheme.palette.primary1Color,
          margin: 0,
        }}
        onLeftIconButtonTouchTap={this.props.onMenuIconTouchTap}
        iconElementRight={toolbar}
      />
    );
  }
}

Header = muiThemeable()(Header);

export default Header;
