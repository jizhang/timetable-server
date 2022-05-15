const { createProxyMiddleware } = require('http-proxy-middleware')
const { createMockMiddleware } = require('./mock-middleware')
const bodyParser = require('body-parser')

module.exports = function (app) {
  if (process.env.MOCK === 'none') {
    const proxy = createProxyMiddleware(['/event', '/note'], {
      target: 'http://127.0.0.1:5001',
    })
    app.use(proxy)
  } else {
    app.use(bodyParser.urlencoded({ extended: false }))
    app.use(bodyParser.json())
    app.use(createMockMiddleware('./mock'))
  }
}
