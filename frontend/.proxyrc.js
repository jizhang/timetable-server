const { createProxyMiddleware } = require('http-proxy-middleware')
const chokidar = require('chokidar')
const glob = require('glob')
const Router = require('routes')

function setupWatcher() {
  const watcher = chokidar.watch('./mock', {
    ignoreInitial: true,
  })

  watcher.on('all', () => {
    console.log('Reload mocks.')
    Object.keys(require.cache)
      .filter((id) => /[\/\\]mock[\/\\]/.test(id))
      .forEach((id) => {
        delete require.cache[id]
      })
  })
}

function createRouter() {
  const router = new Router()

  glob.sync('./mock/**/*.js').forEach((file) => {
    const routes = require(file)
    Object.keys(routes).forEach((path) => {
      router.addRoute(path, routes[path])
    })
  })

  return router
}

function createMockMiddleware() {
  setupWatcher()

  return (req, res, next) => {
    const router = createRouter()
    const m = router.match(req.method + ' ' + req.url)
    if (m) {
      m.fn(req, res, m.params)
    } else {
      next()
    }
  }
}

module.exports = function (app) {
  if (process.env.MOCK === 'none') {
    const proxy = createProxyMiddleware(['/event', '/note'], {
      target: 'http://127.0.0.1:5000',
    })
    app.use(proxy)
  } else {
    app.use(createMockMiddleware())
  }
}
