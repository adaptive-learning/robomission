/**
 * Webpack config for React Components for Jupyter Notebook
 */
var version = require('./package.json').version;
var path = require('path');


// The path for all media, such as css and images. It can be arbitrary,
// but it must match `data_files` setting in `setup.py`.
var mediaPath = 'media/[name].[ext]';


module.exports = [
  {
    entry: './src/jupyter.js',
    output: {
        filename: 'index.js',
        path: path.join(__dirname, '..',  'visualization', 'static'),
        // PublicPath gets prepended to all asset requests.
        // It is dictated by jupyter, which serves extensions files from
        // /nbextensions/<extension-name>/
        publicPath: '/nbextensions/visualization/',
        libraryTarget: 'umd'
    },
    module: {
      strictExportPresence: true,
      rules: [
        {
          // "oneOf" will traverse all following loaders until one will
          // match the requirements. When no loader matches it will fall
          // back to the "file" loader at the end of the loader list.
          oneOf: [
            // "url" loader works just like "file" loader but it also embeds
            // assets smaller than specified size as data URLs to avoid requests.
            {
              test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
              loader: require.resolve('url-loader'),
              options: {
                limit: 10000,
                name: mediaPath,
              },
            },
            // Process JS with Babel.
            {
              test: /\.(js|jsx)$/,
              exclude: /node_modules/,
              loader: 'babel-loader',
              //loader: require.resolve('babel-loader'),
              query: {
                //presets: ['es2015', 'stage-0', 'react'],
                presets: ['env', 'react'],
                plugins: ['transform-object-rest-spread'],
              },
            },
            // The file loader loader doesn't use a "test" so it will catch all
            // modules that fall through the other loaders.
            {
              loader: require.resolve('file-loader'),
              // Exclude `js` files to keep "css" loader working as it injects
              // it's runtime that would otherwise processed through "file" loader.
              // Also exclude `html` and `json` extensions so they get processed
              // by webpacks internal loaders.
              exclude: [/\.js$/, /\.html$/, /\.json$/],
              options: {
                name: mediaPath,
              },
            },
            // ** STOP ** Are you adding a new loader?
            // Make sure to add the new loader(s) before the "file" loader.
          ],
        },
      ],
    },
  }
];
