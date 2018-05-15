import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';
import Joyride from 'react-joyride';
import 'react-joyride/lib/react-joyride-compiled.css';
import { translate } from '../localization';
import { showInstructions, seeInstruction } from '../actions';
import { getScheduledInstructions } from '../selectors/instructions';


const getProps = (state) => ({
  shown: state.instructions.shown,
  scheduledInstructions: getScheduledInstructions(state),
});
const actionCreators = {
  showInstructions,
  seeInstruction: seeInstruction.request,
};

class InstructionsContainer extends React.Component {
  static propTypes = {
    muiTheme: PropTypes.object,
    scheduledInstructions: PropTypes.array,
    shown: PropTypes.bool,
    showInstructions: PropTypes.func,
    seeInstruction: PropTypes.func,
  };

  constructor(props) {
    super(props);
    // this.showInstructions = props.showInstructions.bind(this);
    this.showInstructions = props.showInstructions.bind(this);
    this.seeInstruction = props.seeInstruction.bind(this);
    this.handleJoyrideChange = this.handleJoyrideChange.bind(this);
    this.setInstructions(props.scheduledInstructions);
  }

  componentWillReceiveProps(nextProps) {
    this.setInstructions(nextProps.scheduledInstructions);
  }

  componentDidUpdate(prevProps) {
    if (!prevProps.shown && this.props.shown) {
      this.joyride.reset(true);
    }
  }

  setInstructions(instructions) {
    this.steps = instructions.map(instruction => ({
      text: translate(`instruction.${instruction.id}`),
      selector: instruction.selector,  // '.instructionable-spaceworld',
      position: instruction.position, // 'bottom-left',
      type: 'hover',
      style: {
        mainColor: this.props.muiTheme.palette.primary1Color,
        beacon: {
          // offsetX: 15, offsetY: -20,
          inner: this.props.muiTheme.palette.accent1Color,
          outer: this.props.muiTheme.palette.accent1Color,
        },
      },
    }));
  }

  handleJoyrideChange({ type, index }) {
    switch (type) {
      case 'step:after': {
        const instructionId = this.props.scheduledInstructions[index].id;
        this.seeInstruction(instructionId);
        break;
      }
      case 'finished': {
        this.showInstructions(false);
        break;
      }
      // no default
    }
  }

  render() {
    if (!this.props.shown) {
      return null;
    }
    return (
      <Joyride
        ref={(ref) => { this.joyride = ref; }}
        steps={this.steps}
        type="continuous"
        run={this.props.shown}
        autoStart={this.props.shown}
        showBackButton={true}
        showStepsProgress={true}
        debug={false}
        holePadding={2}
        locale={{
          back: translate('Previous'),
          close: translate('I understand'),
          next: translate('I understand'),
          last: translate('I understand'),
          skip: 'Skip',
        }}
        callback={this.handleJoyrideChange}
      />
    );
  }

}

InstructionsContainer = connect(getProps, actionCreators)(InstructionsContainer);
InstructionsContainer = muiThemeable()(InstructionsContainer);


export default InstructionsContainer;
