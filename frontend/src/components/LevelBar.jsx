import React, { PropTypes } from 'react';
import { Line as ProgressBar } from 'rc-progress';
import muiThemeable from 'material-ui/styles/muiThemeable';


const propTypes = {
  level: PropTypes.number.isRequired,
  activeCredits: PropTypes.number.isRequired,
  maxCredits: PropTypes.number.isRequired,
  percent: PropTypes.number,  // if not set, it's computed from active and max credits
  mini: PropTypes.bool,
};

const defaultProps = {
  mini: false,
};

@muiThemeable()
export default class LevelBar extends React.Component {
  render() {
    const styleDefault = {
      display: 'inline-block',
      width: 250,
      marginLeft: 8,
      marginRight: 8,
    };
    const styleMini = {
      display: 'inline-block',
      width: 50,
      marginLeft: 8,
      fontSize: 12,
      lineHeight: '9px',
      textAlign: 'center',
    };
    let percent = this.props.percent;
    if (percent === undefined || percent === null) {
      percent = Math.floor(100 * this.props.activeCredits / this.props.maxCredits);
    }
    if (this.props.mini) {
      return (
        <span>
          <span style={{ fontSize: 18 }}>
            L{ this.props.level }
          </span>
          <span style={styleMini}>
            {this.props.activeCredits} / {this.props.maxCredits}
            <ProgressBar
              percent={percent}
              strokeWidth={8}
              strokeColor="#E3E3E3"
              trailColor="#F3F3F3"
            />
          </span>
        </span>
      );
    }
    return (
      <span>
        <span style={{ fontSize: 18 }}>
          L{ this.props.level }
        </span>
        <span style={styleDefault}>
          <ProgressBar
            percent={percent}
            strokeWidth={5}
            trailWidth={5}
            strokeColor={this.props.muiTheme.palette.accent2Color}
            trailColor="#a3a3a3"
          />
        </span>
        {this.props.activeCredits} / {this.props.maxCredits}
      </span>
    );
  }
}


LevelBar.propTypes = propTypes;
LevelBar.defaultProps = defaultProps;
