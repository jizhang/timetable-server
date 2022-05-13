const { createProxyMiddleware } = require('http-proxy-middleware')
const chokidar = require('chokidar')
const Router = require('routes')

module.exports = function (app) {
  if (process.env.MOCK === 'none') {
    const apiProxy = createProxyMiddleware(['/event', '/note'], {
      target: 'http://127.0.0.1:5000',
    })
    app.use(apiProxy)
  } else {
    const watcher = chokidar.watch('./mock')
    watcher.on('ready', function() {
      watcher.on('all', function() {
        console.log("Clearing ./mock module cache from server")
        Object.keys(require.cache).forEach(function(id) {
          if (/[\/\\]mock[\/\\]/.test(id)) {
            delete require.cache[id]
            console.log(id)
          }
        })
      })
    })

    app.use((req, res, next) => {
      const mockRoutes = require('./mock')

      const router = new Router()

      Object.keys(mockRoutes).forEach((path) => {
        router.addRoute(path, mockRoutes[path])
      })

      const m = router.match(req.method + ' ' + req.url)
      if (m) m.fn(req, res, m.params)
      else next()
    })
  }
}
