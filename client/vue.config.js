module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: process.env.API_PROXY,
        secure: false,
        timeout: 86400 * 1000,
        proxyTimeout: 86400 * 1000,
        onProxyReq: (proxyReq, req, res) => req.setTimeout(86400 * 1000)
      },
      '/girder': {
        target: "http://localhost:8080",
        secure: false,
        timeout: 86400 * 1000,
        proxyTimeout: 86400 * 1000,
        onProxyReq: (proxyReq, req, res) => req.setTimeout(86400 * 1000)
      }
    },
    useLocalIp: true,
    public: "localhost:8080"
  },
  baseUrl: process.env.NODE_ENV === 'production'
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
