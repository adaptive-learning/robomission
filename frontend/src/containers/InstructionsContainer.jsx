import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';
import HelpIcon from 'material-ui/svg-icons/action/help';
import IconButton from 'material-ui/IconButton';
import Joyride from 'react-joyride';
import 'react-joyride/lib/react-joyride-compiled.css';
import { translate } from '../localization';
import { showInstructions, seeInstruction } from '../actions/instructions';
import { inMode } from '../selectors/app';
import { getScheduledInstructions } from '../selectors/instructions';


const getProps = (state) => ({
  activeInstructionIndex: state.instructions.activeIndex,
  scheduledInstructions: getScheduledInstructions(state),
  showInstructionsButton: inMode(state, 'task') && getScheduledInstructions(state).length > 0,
});
const actionCreators = { showInstructions, seeInstruction };

@connect(getProps, actionCreators)
@muiThemeable()
class InstructionsContainer extends React.Component {
  static propTypes = {
    muiTheme: PropTypes.object,
    scheduledInstructions: PropTypes.array,
    activeInstructionIndex: PropTypes.number,
    showInstructions: PropTypes.func,
    seeInstruction: PropTypes.func,
  };

  constructor(props) {
    super(props);
    // this.showInstructions = props.showInstructions.bind(this);
    this.showInstructions = () => {
      if (this.props.activeInstructionIndex == null) {
        this.props.showInstructions();
      }
    };
    this.seeInstruction = props.seeInstruction.bind(this);
    this.handleJoyrideChange = this.handleJoyrideChange.bind(this);
    this.setInstructions(props.scheduledInstructions);
  }

  componentWillReceiveProps(nextProps) {
    this.setInstructions(nextProps.scheduledInstructions);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.activeInstructionIndex === null && this.props.activeInstructionIndex !== null) {
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
      // no default
    }
  }

  renderShowInstructionsButton() {
    if (!this.props.showInstructionsButton) {
      return null;
    }
    const blocklyTrashcanColor = '#576065';
    return (
      <IconButton
        onTouchTap={this.showInstructions}
        style={{
          position: 'fixed',
          bottom: 31,
          right: 110,
          zIndex: 100,
          width: 60,
          height: 60,
          padding: 0,
        }}
        iconStyle={{
          width: 60,
          height: 60,
        }}
      >
        <HelpIcon color={blocklyTrashcanColor} hoverColor="#fff" />
      </IconButton>
    );
  }

  render() {
    const active = this.props.activeInstructionIndex != null;
    return (
      <div>
        <Joyride
          ref={(ref) => { this.joyride = ref; }}
          steps={this.steps}
          type="continuous"
          run={active}
          autoStart={active}
          showBackButton={false}
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
        { this.renderShowInstructionsButton() }
      </div>
    );
  }

}


export default InstructionsContainer;
