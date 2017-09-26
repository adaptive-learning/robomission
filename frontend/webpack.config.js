var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker');


module.exports = {
    context: __dirname,
    entry: [
        'babel-polyfill',
        './src/index',
    ],

    output: {
        path: path.resolve('./static/'),
        filename: 'bundles/main.js',
        publicPath: '/static/'
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
    ],

    module: {
        loaders: [
            // JSX
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel',
                query: {
                  presets: ['es2015', 'stage-0', 'react'],
                  plugins: ['transform-decorators-legacy']
                }
            },

            // CSS
            {
                test: /\.css$/,
                loader: "style-loader!css-loader"
            },

            // Images
            { test: /\.(png|jpg)$/,  loader: "url-loader?limit=8000&name=/images/[name].[ext]" },
            { test: /\.woff|woff2$/,  loader: "url-loader?limit=10000&mimetype=application/font-woff&name=/fonts/[name].[ext]" },
            { test: /\.ttf|eot|svg$/,    loader: "file-loader" }
        ]
    },

    resolve: {
        modulesDirectories: ['node_modules'],
        extensions: ['', '.js', '.jsx'],
        alias:{
            images: path.resolve('./assets/images')
        }
    }
}
