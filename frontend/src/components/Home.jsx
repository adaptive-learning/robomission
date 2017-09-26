import React from 'react';
import { Link } from 'react-router';
import muiThemeable from 'material-ui/styles/muiThemeable';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import Paper from 'material-ui/Paper';
import RaisedButton from 'material-ui/RaisedButton';
import ArrowDown from 'material-ui/svg-icons/hardware/keyboard-arrow-down';
import Scroll from 'react-scroll';
import SpaceGameContainer from '../containers/SpaceGameContainer';
import TaskEnvironmentContainer from '../containers/TaskEnvironmentContainer';
import NextTaskButtonContainer from '../containers/NextTaskButtonContainer';
import neuronsBackgroundPath from 'images/neurons-tile.png';
import fiBackgroundPath from 'images/fi-slide.jpg';


@muiThemeable()
export default class Home extends React.Component {
  renderSlide({ style, content, footer }, index) {
    return (
      <Scroll.Element key={index} name={`intro-slide-${index}`}>
        <section
          style={{
            ...slideStyle,
            height: (index === 0) ? '90vh' : '100vh',
            ...style,
          }}
        >
          <div style={{ display: 'table-row' }}>
            <div style={slideContentStyle}>
              {content}
            </div>
          </div>
          {footer && (
            <div style={slideFooterStyle}>
              {footer}
            </div>
          )}
        </section>
      </Scroll.Element>
    );
  }

  render() {
    const slides = [
      // slide 0
      {
        style: {
          backgroundImage: `url(/static/images/background-space.png)`,
          backgroundSize: '500px auto',
          backgroundColor: '#111122',
          color: '#fff',
        },
        content: (
          <Paper
            style={{
              display: 'inline-block',
              paddingTop: 10,
              paddingBottom: 35,
              paddingLeft: 50,
              paddingRight: 50,
              minWidth: 500,
              backgroundColor: 'rgba(50, 50, 50, 0.9)',
            }}
            zDepth={2}
          >
            <h2>Nauč se programovat!</h2>
            <span style={{ marginRight: 20 }}>
              <NextTaskButtonContainer />
            </span>
            <Link to="/tasks">
              <RaisedButton label="Přehled úloh" />
            </Link>
          </Paper>
        ),
        footer: (
          <Scroll.Link to="intro-slide-1" smooth={true} duration={500}>
            <FloatingActionButton secondary={true}>
              <ArrowDown />
            </FloatingActionButton>
          </Scroll.Link>
        ),
      },
      // slide 1
      {
        style: {
          backgroundColor: this.props.muiTheme.palette.canvasColor,
          color: '#fff',
        },
        content: (
          <div>
            <h2>Prozkoumej tajemný vesmír<br />a posbírej všechny diamanty</h2>
            <div>
              <SpaceGameContainer
                taskEnvironmentId="home-commands"
                controls={['fly', 'left', 'right', 'reset']}
              />
            </div>
            <p style={{ visibility: this.props.spaceWorldDemoSolved ? 'visible' : 'hidden' }}>
              Skvěle, úloha vyřešena!
            </p>
          </div>
        ),
        footer: (
          <Scroll.Link to="intro-slide-2" smooth={true} duration={500}>
            <FloatingActionButton secondary={true} disabled={!this.props.spaceWorldDemoSolved}>
              <ArrowDown />
            </FloatingActionButton>
          </Scroll.Link>
        ),
      },
      // slide 2
      {
        style: {
          backgroundColor: this.props.muiTheme.palette.primary1Color,
        },
        content: (
          <div>
            <h2>Nauč se ovládat vesmírnou loď<br />pomocí počítačových programů</h2>
            <div
              style={{
                position: 'relative',
                height: 350,
                width: 800,
                margin: '0 auto',
                border: '2px solid #777'
              }}
            >
              <TaskEnvironmentContainer taskEnvironmentId="home-program" />
            </div>
            <p style={{ visibility: this.props.programDemoSolved ? 'visible' : 'hidden' }}>
              Skvěle, úloha vyřešena!
            </p>
          </div>
        ),
        footer: (
          <Scroll.Link to="intro-slide-3" smooth={true} duration={500}>
            <FloatingActionButton secondary={true} disabled={!this.props.programDemoSolved}>
              <ArrowDown />
            </FloatingActionButton>
          </Scroll.Link>
        ),
      },
      // slide 3
      {
        style: {
          backgroundImage: `url(${neuronsBackgroundPath})`,
        },
        content: (
          <div>
            <h2>Hra je poháněna umělou inteligencí,<br />díky které se hra přizpůsobuje tvým dovednostem</h2>
          </div>
        ),
        footer: (
          <Scroll.Link to="intro-slide-4" smooth={true} duration={500}>
            <FloatingActionButton secondary={true}>
              <ArrowDown />
            </FloatingActionButton>
          </Scroll.Link>
        ),
      },
      // slide 4
      {
        style: {
          backgroundImage: `url(${fiBackgroundPath})`,
          backgroundSize: 'cover',
        },
        content: (
          <Paper
            style={{
              display: 'inline-block',
              paddingTop: 10,
              paddingBottom: 40,
              paddingLeft: 50,
              paddingRight: 50,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
            }}
            zDepth={1}
          >
            <h2>Aplikaci vyvíjí tým Adaptabilního učení<br />na Fakultě informatiky Masarykovy Univerzity</h2>
            <span style={{ marginRight: 20 }}>
              <a href="https://www.fi.muni.cz/adaptivelearning/?a=projects" target="_blank" rel="noreferrer noopener">
                <RaisedButton label="Laboratoř adaptabilního učení" />
              </a>
            </span>
            <a href="https://www.fi.muni.cz/about/index.xhtml.cs" target="_blank" rel="noreferrer noopener">
              <RaisedButton label="Fakulta informatiky MU" style={{ minWidth: 265 }} />
            </a>
          </Paper>
        ),
        footer: (
          <Scroll.Link to="intro-slide-5" smooth={true} duration={500}>
            <FloatingActionButton secondary={true}>
              <ArrowDown />
            </FloatingActionButton>
          </Scroll.Link>
        ),
      },
      // slide 5
      {
        style: {
          backgroundImage: `url(/static/images/background-space.png)`,
          backgroundSize: '500px auto',
          backgroundColor: '#111122',
          color: '#fff',
        },
        content: (
          <div>
            <h2>Vyleť do vesmíru!</h2>
            <NextTaskButtonContainer />
          </div>
        ),
      },
    ];
    return (
      <div style={longPageStyle}>
        {slides.map(this.renderSlide)}
      </div>
    );
  }
}

const longPageStyle = {
  width: '100%',
  height: '100%',
  margin: 0,
};

const slideStyle = {
  width: '100%',
  padding: '0 7%',
  display: 'table',
  margin: 0,
  height: '100vh',
};

const slideContentStyle = {
  display: 'table-cell',
  verticalAlign: 'middle',
  maxWidth: 1000,
  margin: '20px auto',
  textAlign: 'center',
  lineHeight: 1.3,
};


const slideFooterStyle = {
  display: 'table-row',
  verticalAlign: 'bottom',
  maxWidth: 1000,
  margin: '0 auto',
  height: 90,
  textAlign: 'center',
};
