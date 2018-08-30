module.exports = {
  devServer: {
    proxy: process.env.API_PROXY,
    useLocalIp: true,
    public: "localhost:8080"
  },
  chainWebpack: config => {
    config.module
      .rule('js')
      .include
      .add('resonantgeo')
  }
}
