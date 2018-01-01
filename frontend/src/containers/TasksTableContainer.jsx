import React from 'react';
import { connect } from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';
import TasksTable from '../components/TasksTable';
import { fetchPracticeOverview } from '../actions';
import { isPracticeOverviewInvalidated } from '../selectors/app';
import { getPracticeOverviewUrl } from '../selectors/student';
import LongPage from '../components/LongPage';


function getProps(state) {
  return {
    tasks: state.tasks,
    categories: state.categories,
    recommendation: state.recommendation,
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
    const { tasks, categories } = this.props;
    const allCategoryIds = Object.keys(categories);
    const compareCategoryIds = (a, b) => categories[a].level - categories[b].level;
    const orderedCategoryIds = allCategoryIds.sort(compareCategoryIds);
    const tasksInCategories = orderedCategoryIds.map(categoryId => ({
      category: categories[categoryId],
      tasks: categories[categoryId].tasks.map(id => tasks[id]),
    }));

    return (
      <LongPage>
        <TasksTable
          tasksInCategories={tasksInCategories}
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
