import React from 'react';
import { storiesOf, action, linkTo, addDecorator } from '@kadira/storybook';
import { muiTheme } from 'storybook-addon-material-ui';
import Welcome from './Welcome';
import BlocklyEditor from '../components/BlocklyEditor';
import CodeEditor from '../components/CodeEditor';
import FlocsProvider from '../FlocsProvider';
import SpaceGame from '../components/SpaceGame';
import TasksTable from '../components/TasksTable';
import SpaceGameContainer from '../containers/SpaceGameContainer';
import TaskEditorContainer from '../containers/TaskEditorContainer';
import TaskEnvironmentContainer from '../containers/TaskEnvironmentContainer';
import { parseSpaceWorld } from '../core/spaceWorldDescription';
import { globalConfiguration, configureStore } from '../config';
import { setTask, setEditorType } from '../actions/taskEnvironment';
import { theme } from '../theme';

globalConfiguration();

addDecorator(muiTheme([theme]));

const store = configureStore();
addDecorator((story) => (
  <FlocsProvider store={store}>
    {story()}
  </FlocsProvider>
));


storiesOf('Welcome', module)
  .add('to Storybook', () => (
    <Welcome showApp={linkTo('CodeEditor')}/>
  ));


storiesOf('BlocklyEditor', module)
  .add('fixed size', () => (
    <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, right: 0 }} >
      <div style={{ backgroundColor: 'blue', height: '50px', width: '100%' }} />
      <span
        style={{
          display: 'inline-block',
          position: 'absolute',
          backgroundColor: 'red',
          top: '50px',
          bottom: '0px',
          left: '0px',
          right: '300px',
        }}
      >
        <BlocklyEditor
          onChange={action('onChange')}
        />
      </span>
      <span
        style={{
          display: 'inline-block',
          position: 'absolute',
          right: 0,
          width: '300px',
          top: '50px',
          bottom: 0,
          backgroundColor: 'yellow',
        }}
      />
    </div>
  ));


storiesOf('CodeEditor', module)
  .add('fixed size', () => (
    <div style={{ position: 'absolute', width: 600, height: 600 }}>
      <CodeEditor
        code="print('Los Karlos was here!')"
        onChange={action('onChange')}
      />
    </div>
  ))
  .add('full screen', () => (
    <div style={{ position: 'absolute', top: 0, bottom: 0, width: '100%' }}>
      <CodeEditor
        code="print('Where is the punched pocket?')"
        onChange={action('onChange')}
      />
    </div>
  ));


storiesOf('SpaceGame', module)
  .add('initial', () => (
    <SpaceGame
      gameState={{
        fields: parseSpaceWorld(`\
          |b |bM|b |b |b |
          |k |k |kD|kA|k |
          |kA|k |k |k |k |
          |k |kM|kD|k |k |
          |k |k |kS|k |kM|`),
        stage: 'initial',
        diamonds: { taken: 0, total: 2 },
        energy: { current: 2, full: 2 },
      }}
    />
  ))
  .add('solved', () => (
    <SpaceGame
      gameState={{
        fields: parseSpaceWorld(`\
          |b |bM|bS|b |b |
          |k |k |k |kA|k |
          |kA|k |k |k |k |
          |k |kM|k |k |k |
          |k |k |k |k |kM|`),
        stage: 'solved',
        diamonds: { taken: 2, total: 2 },
        energy: { current: 1, full: 2 },
      }}
    />
  ))
  .add('with some controls', () => (
    <SpaceGame
      gameState={{
        fields: parseSpaceWorld(`\
          |b |bM|b |b |b |
          |k |k |kD|kA|k |
          |kA|k |k |k |k |
          |k |kM|kD|k |k |
          |k |k |kS|k |kM|`),
        stage: 'initial',
        diamonds: { taken: 0, total: 2 },
        energy: { current: 2, full: 2 },
      }}
      controls={['fly', 'left', 'right', 'reset']}
      onControlClicked={action('onControlClicked')}
    />
  ))
  .add('SpaceGameContainer', () => {
    const task = {
      taskId: 'two-steps-forward',
      categoryId: 'moves',
      setting: {
        fields: parseSpaceWorld(`
          |b |b |b |b |b |
          |k |k |k |k |k |
          |k |k |kS|k |k |`),
      },
    };
    store.dispatch(setTask('demo', task));
    return (
      <SpaceGameContainer
        taskEnvironmentId="demo"
        controls={['fly', 'left', 'right', 'reset']}
      />
    );
  });


storiesOf('TaskEnvironment', module)
  .add('default', () => {
    const task = {
      taskId: 'two-steps-forward',
      categoryId: 'moves',
      setting: {
        fields: parseSpaceWorld(`
          |b |b |b |b |b |
          |k |k |k |k |k |
          |k |k |kS|k |k |`),
      },
    };
    store.dispatch(setTask('demo', task));
    return (
      <TaskEnvironmentContainer taskEnvironmentId="demo" />
    );
  })
  .add('all controls', () => {
    const task = {
      taskId: 'two-steps-forward',
      categoryId: 'moves',
      setting: {
        fields: parseSpaceWorld(`
          |b |b |b |b |b |
          |k |k |k |k |k |
          |k |k |kS|k |k |`),
      },
    };
    store.dispatch(setTask('demo', task));
    return (
      <TaskEnvironmentContainer
        taskEnvironmentId="demo"
        controls={['fly', 'left', 'right', 'shoot', 'run', 'reset']}
      />
    );
  })
  .add('code editor', () => {
    const task = {
      taskId: 'two-steps-forward',
      categoryId: 'moves',
      setting: {
        fields: parseSpaceWorld(`
          |b |b |b |b |b |
          |k |k |k |k |k |
          |k |k |kS|k |k |`),
      },
    };
    store.dispatch(setTask('demo-code-editor', task));
    store.dispatch(setEditorType('demo-code-editor', 'code'));
    return (
      <TaskEnvironmentContainer taskEnvironmentId="demo-code-editor" />
    );
  });


storiesOf('TaskEditor', module)
  .add('TaskEditorContainer', () => (
    <TaskEditorContainer />
  ));


storiesOf('TasksTable', module)
  .add('default', () => {
    const tasks = [
      {
        taskId: 'one-step-forward',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'two-steps-forward',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'three-steps-forward',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'turning-left',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'turning-right',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'turning-left-and-right',
        categoryId: 'moves',
        setting: {},
      },
      {
        taskId: 'ladder',
        categoryId: 'repeat',
        setting: {},
      },
      {
        taskId: 'zig-zag',
        categoryId: 'repeat',
        setting: {},
      },
    ];
    return (
      <TasksTable tasks={tasks} urlBase="/task/" />
    );
  });
