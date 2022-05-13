const { createProxyMiddleware } = require('http-proxy-middleware')
const { createMockMiddleware } = require('./mock-middleware')

module.exports = function (app) {
  if (process.env.MOCK === 'none') {
    const proxy = createProxyMiddleware(['/event', '/note'], {
      target: 'http://127.0.0.1:5000',
    })
    app.use(proxy)
  } else {
    app.use(createMockMiddleware('./mock'))
  }
}
