// const CopyWebpackPlugin = require("copy-webpack-plugin");
// const webpack = require("webpack");
// const path = require("path");

// let cesiumSource = "./node_modules/cesium/Source";
// let cesiumWorkers = "../Build/Cesium/Workers";

module.exports = {
  devServer: {
    port: 8081,
    useLocalIp: true,
    public: process.env.PUBLIC_ADDRESS,
    proxy: {
      "/api": {
        target: process.env.API_PROXY,
        secure: false
      }
    }
  },
  publicPath: process.env.NODE_ENV === "production" ? "/static/external/" : "/",
  // configureWebpack: {
  //   plugins: [
  //     new CopyWebpackPlugin([
  //       { from: path.join(cesiumSource, cesiumWorkers), to: "Workers" }
  //       { from: path.join(paths.cesiumSource, '../Build/Cesium/ThirdParty/Workers'), to: 'ThirdParty/Workers' }
  //     ]),
  //     new CopyWebpackPlugin([
  //       { from: path.join(cesiumSource, "Assets"), to: "Assets" }
  //     ]),
  //     new CopyWebpackPlugin([
  //       { from: path.join(cesiumSource, "Widgets"), to: "Widgets" }
  //     ]),
  //     new webpack.DefinePlugin({
  //       // Define relative base path in cesium for loading assets
  //       CESIUM_BASE_URL: JSON.stringify("")
  //     })
  //   ],
  //   resolve: {
  //     alias: {
  //       // CesiumJS module name
  //       cesium: path.resolve(__dirname, cesiumSource)
  //     }
  //   }
  // },
  chainWebpack: config => {
    config.module
      .rule("js")
      .include.add(/^resonantgeo$/)
      .end()
      .use()
      .loader("babel-loader");

    config.module
      .rule("glsl")
      .test(/\.glsl$/)
      .include.add(/vtk\.js(\/|\\)/)
      .end()
      .use()
      .loader("shader-loader");
  }
};
