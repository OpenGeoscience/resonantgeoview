module.exports = {
  devServer: {
    port: 8081,
    useLocalIp: true,
    public: process.env.PUBLIC_ADDRESS,
    proxy: {
      '/api': {
        target: process.env.API_PROXY,
        secure: false
      }
    }
  },
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/external/'
    : '/',
  chainWebpack: config => {
    config.module
      .rule('js')
      .include
      .add(/^resonantgeo$/)
      .end()
      .use()
      .loader('babel-loader')
  }
}
