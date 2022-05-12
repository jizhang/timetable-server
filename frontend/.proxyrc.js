const { createProxyMiddleware } = require('http-proxy-middleware')
const Router = require('routes')
const mockRoutes = require('./mock')

module.exports = function (app) {
  if (process.env.MOCK === 'none') {
    const apiProxy = createProxyMiddleware(['/event', '/note'], {
      target: 'http://127.0.0.1:5000',
    })
    app.use(apiProxy)
  } else {
    const router = new Router()

    Object.keys(mockRoutes).forEach((path) => {
      router.addRoute(path, mockRoutes[path])
    })

    app.use((req, res, next) => {
      const m = router.match(req.method + ' ' + req.url)
      if (m) m.fn(req, res, m.params)
      else next()
    })
  }
}
