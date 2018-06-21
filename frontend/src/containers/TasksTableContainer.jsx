import React from 'react';
import { connect } from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';
import TasksTable from '../components/TasksTable';
import { fetchPracticeOverview } from '../actions';
import { isPracticeOverviewInvalidated } from '../selectors/app';
import { getPracticeOverviewUrl, getLevelStatus } from '../selectors/student';
import { getMissionList } from '../selectors/problemSets';
import LongPage from '../components/LongPage';


function getProps(state) {
  return {
    missions: getMissionList(state),
    recommendation: state.recommendation,
    levelStatus: getLevelStatus(state),
    isPracticeOverviewInvalidated: isPracticeOverviewInvalidated(state),
    practiceOverviewUrl: getPracticeOverviewUrl(state),
  };
}

const actionCreators = {
  fetchPracticeOverview: fetchPracticeOverview.request
};

class TasksTableContainer extends React.Component {
  componentWillMount() {
    // make sure to load updated practiceOverivew on transition to this page
    if (this.props.isPracticeOverviewInvalidated) {
      this.props.fetchPracticeOverview(this.props.practiceOverviewUrl);
    }
  }

  componentDidUpdate(prevProps) {
    // currently, practiceOverview is loaded anyway (on all pages)
    //if (!prevProps.isLoaded && this.props.isLoaded) {
    //  this.props.fetchPraticeOverview();
    //}
  }

  render() {
    return (
      <LongPage>
        <TasksTable
          missions={this.props.missions}
          levelStatus={this.props.levelStatus}
          urlBase="/task/"
          recommendation={this.props.recommendation}
        />
      </LongPage>
    );
  }
}

TasksTableContainer = muiThemeable()(TasksTableContainer);
TasksTableContainer = connect(getProps, actionCreators)(TasksTableContainer);

export default TasksTableContainer;
