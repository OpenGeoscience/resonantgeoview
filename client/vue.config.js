var webpack = require("webpack");

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
  publicPath: process.env.VUE_APP_STATIC_PATH,
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
  },
  configureWebpack: () => {
    return {
      plugins: [
        new webpack.DefinePlugin({
          "process.env": {
            VERSION: JSON.stringify(require("./package.json").version)
          }
        })
      ]
    };
  }
};
