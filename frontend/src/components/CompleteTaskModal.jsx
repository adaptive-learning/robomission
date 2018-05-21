import React from 'react';
import { Link } from 'react-router-dom';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import NextTaskButtonContainer from '../containers/NextTaskButtonContainer';
import LevelBar from '../components/LevelBar';
import Text from '../localization/Text';
import { translate } from '../localization';


export default class CompleteTaskModal extends React.Component {
  constructor(props) {
    super();
    const { activeCredits, maxCredits } = props.levelStatus;
    this.state = {
      shownPercent: Math.floor(100 * activeCredits / maxCredits),
      shownCredits: activeCredits,
      animating: false,
    };
    this.animationTimer = null;
    this.showLevelProgress = props.showLevelProgress.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.levelStatus.level !== this.props.levelStatus.level) {
      this.setState({ shownPercent: 0, shownCredits: 0, animating: true }, () => {
        // immediately update state again to avoid "decrease" animation
        this.setState({ shownPercent: 1 });
      });
    }
    if (!this.state.animating && nextProps.levelStatus.hasNext) {
      this.setState({ animating: true });
    }
    if (this.state.animating && !nextProps.levelStatus.hasNext) {
      this.setState({ animating: false });
    }
  }

  componentDidUpdate(prevProps) {
    if (!prevProps.open && this.props.open && this.props.levelStatus.hasNext) {
      this.showLevelProgress(this.props.levelProgress);
    }
    if (prevProps.levelStatus.activeCredits !== this.props.levelStatus.activeCredits) {
      this.animateProgress();
    }
  }


  animateProgress() {
    const { activeCredits, maxCredits } = this.props.levelStatus;
    // clear any pending animation before starting a new one
    clearTimeout(this.animationTimer);
    const initialPause = 600;
    const stepPause = 15;
    const increaseBy1 = () => {
      if (this.state.shownCredits >= this.props.levelStatus.activeCredits) {
        clearTimeout(this.animationTimer);
        this.setState({ credits: activeCredits, animating: false });
        return;
      }
      const shownPercent = this.state.shownPercent + 1;
      const shownCredits = Math.min(activeCredits, Math.floor(maxCredits * shownPercent / 100));
      this.setState({ shownPercent, shownCredits });
      this.animationTimer = setTimeout(increaseBy1, stepPause);
    };
    this.animationTimer = setTimeout(increaseBy1, initialPause);
  }

  renderContinueButton(active = true) {
    return (
      <RaisedButton
        label="Pokračovat"
        primary={true}
        onClick={this.showLevelProgress}
        disabled={!active}
      />
    );
  }

  render() {
    let actions = [];
    let bottomMessage = null;
    if (this.props.levelStatus.hasNext && !this.state.animating) {
      actions = [this.renderContinueButton(true)];
    } else if (this.state.animating) {
      actions = [this.renderContinueButton(false)];
    } else {
      if (this.props.recommendation.isEasy) {
        bottomMessage = <Text id="easy-task-challenge" />
      }
      actions = [
        <NextTaskButtonContainer />,
        <Link to="/tasks">
          <RaisedButton label={<Text id="Tasks" />} style={{ marginLeft: 10 }} />
        </Link>
      ];
    }
    return (
      <Dialog
        title={translate('excellent-task-solved')}
        actions={actions}
        open={this.props.open}
        onRequestClose={this.props.handleClose}
        contentStyle={{ textAlign: 'center' }}
        actionsContainerStyle={{ textAlign: 'center', paddingBottom: 20, minHeight: 80 }}
      >
        <LevelBar
          level={this.props.levelStatus.level}
          activeCredits={this.state.shownCredits}
          maxCredits={this.props.levelStatus.maxCredits}
          percent={this.state.shownPercent}
        />
        {bottomMessage && (
          <div style={{ marginTop: 25 }}>
            {bottomMessage}
          </div>
        )}
      </Dialog>
    );
  }
}
