// you can use this file to add your custom webpack plugins, loaders and anything you like.
// This is just the basic way to add addional webpack configurations.
// For more information refer the docs: https://getstorybook.io/docs/configurations/custom-webpack-config

// IMPORTANT
// When you add this file, we won't add the default configurations which is similar
// to "React Create App". This only has babel loader to load JavaScript.

module.exports = {
  plugins: [
    // your custom plugins
  ],
  module: {
    loaders: [
      { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel',
        query: {
          presets: ['es2015', 'stage-0', 'react', 'react-hmre'],
          plugins: ['transform-decorators-legacy']
        }
      },
      { test: /\.css$/, loader: "style-loader!css-loader" },
      { test: /\.(png)$/, loader: "url-loader?limit=8000&name=images/[name].[ext]" },
      { test: /\.woff|woff2$/, loader: "url-loader?limit=10000&mimetype=application/font-woff&name=fonts/[name].[ext]" },
      { test: /\.ttf|eot|svg$/, loader: "file-loader" }
    ],
  },
};
