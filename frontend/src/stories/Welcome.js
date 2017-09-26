import React from 'react';

const styles = {
  main: {
    margin: 15,
    maxWidth: 600,
    lineHeight: 1.4,
    fontFamily: '"Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif',
  },

  logo: {
    width: 200,
  },

  link: {
    color: '#1474f3',
    textDecoration: 'none',
    borderBottom: '1px solid #1474f3',
    paddingBottom: 2,
  },

  code: {
    fontSize: 15,
    fontWeight: 600,
    padding: "2px 5px",
    border: "1px solid #eae9e9",
    borderRadius: 4,
    backgroundColor: '#f3f2f2',
    color: '#3a3a3a',
  },

  note: {
    opacity: 0.5,
  }
};

export default class Welcome extends React.Component {
  showApp(e) {
    e.preventDefault();
    if(this.props.showApp) this.props.showApp();
  }

  render() {
    return (
      <div style={styles.main}>
        <h1>Flocs Storybook</h1>
        <p>
          Stories are visual tests for React components.
          Each story shows a single state of one or more components.
          You can edit those components and see changes right away.
          Stories are defined inside <code style={styles.code}>stories</code> directory.
        </p>
        <div style={styles.note}>
          <b>NOTES:</b>
          <ul>
            <li>
            Have a look at the <code style={styles.code}>.storybook/webpack.config.js</code> to add webpack
            loaders and plugins you are using in this project.
            </li>
            <li>
            See these sample <a style={styles.link} href='#' onClick={this.showApp.bind(this)}>stories</a>.
            </li>
            <li>
            Have a look at the <a style={styles.link} href="https://github.com/kadirahq/react-storybook" target="_blank">React Storybook</a> repo for more information.
            </li>
          </ul>
        </div>
      </div>
    );
  }
}
