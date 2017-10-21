import React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';
import { Button, Welcome } from '@storybook/react/demo';

//import BlocklyEditor from '../components/BlocklyEditor';
//import CodeEditor from '../components/CodeEditor';
//import SpaceGame from '../components/SpaceGame';
//import TasksTable from '../components/TasksTable';
//import { parseSpaceWorld } from '../core/spaceWorldDescription';

storiesOf('Welcome', module).add('to Storybook', () => <Welcome showApp={linkTo('Button')} />);

storiesOf('Button', module)
  .add('with text', () => <Button onClick={action('clicked')}>Hello Button</Button>)
  .add('with some emoji', () => <Button onClick={action('clicked')}>😀 😎 👍 💯</Button>);


//storiesOf('BlocklyEditor', module)
//  .add('fixed size', () => (
//    <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, right: 0 }} >
//      <div style={{ backgroundColor: 'blue', height: '50px', width: '100%' }} />
//      <span
//        style={{
//          display: 'inline-block',
//          position: 'absolute',
//          backgroundColor: 'red',
//          top: '50px',
//          bottom: '0px',
//          left: '0px',
//          right: '300px',
//        }}
//      >
//        <BlocklyEditor
//          onChange={action('onChange')}
//        />
//      </span>
//      <span
//        style={{
//          display: 'inline-block',
//          position: 'absolute',
//          right: 0,
//          width: '300px',
//          top: '50px',
//          bottom: 0,
//          backgroundColor: 'yellow',
//        }}
//      />
//    </div>
//  ));
//
//
//storiesOf('CodeEditor', module)
//  .add('fixed size', () => (
//    <div style={{ position: 'absolute', width: 600, height: 600 }}>
//      <CodeEditor
//        code="print('Los Karlos was here!')"
//        onChange={action('onChange')}
//      />
//    </div>
//  ))
//  .add('full screen', () => (
//    <div style={{ position: 'absolute', top: 0, bottom: 0, width: '100%' }}>
//      <CodeEditor
//        code="print('Where is the punched pocket?')"
//        onChange={action('onChange')}
//      />
//    </div>
//  ));
//
//
//storiesOf('SpaceGame', module)
//  .add('initial', () => (
//    <SpaceGame
//      gameState={{
//        fields: parseSpaceWorld(`\
//          |b |bM|b |b |b |
//          |k |k |kD|kA|k |
//          |kA|k |k |k |k |
//          |k |kM|kD|k |k |
//          |k |k |kS|k |kM|`),
//        stage: 'initial',
//        diamonds: { taken: 0, total: 2 },
//        energy: { current: 2, full: 2 },
//      }}
//    />
//  ))
//  .add('solved', () => (
//    <SpaceGame
//      gameState={{
//        fields: parseSpaceWorld(`\
//          |b |bM|bS|b |b |
//          |k |k |k |kA|k |
//          |kA|k |k |k |k |
//          |k |kM|k |k |k |
//          |k |k |k |k |kM|`),
//        stage: 'solved',
//        diamonds: { taken: 2, total: 2 },
//        energy: { current: 1, full: 2 },
//      }}
//    />
//  ))
//  .add('with some controls', () => (
//    <SpaceGame
//      gameState={{
//        fields: parseSpaceWorld(`\
//          |b |bM|b |b |b |
//          |k |k |kD|kA|k |
//          |kA|k |k |k |k |
//          |k |kM|kD|k |k |
//          |k |k |kS|k |kM|`),
//        stage: 'initial',
//        diamonds: { taken: 0, total: 2 },
//        energy: { current: 2, full: 2 },
//      }}
//      controls={['fly', 'left', 'right', 'reset']}
//      onControlClicked={action('onControlClicked')}
//    />
//  ));
