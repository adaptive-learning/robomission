/**
 * Main module for exporting React Component for use in Jupyter Notebooks.
 */
import JupyterReact from 'jupyter-react-js';
import components from './components';

function load_ipython_extension () {
  requirejs([
    "base/js/namespace",
    "base/js/events",
  ], function( Jupyter, events ) {
    JupyterReact.init( Jupyter, events, 'react.components', { components, save: false } );
  });
}

module.exports = {
  load_ipython_extension: load_ipython_extension
};
