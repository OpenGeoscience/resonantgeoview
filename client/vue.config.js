module.exports = {
  devServer: {
    proxy: process.env.API_PROXY,
    useLocalIp: true
  },
  chainWebpack: config => {
    config.module
      .rule('js')
      .include
      .add('resonantgeo')
  }
}
