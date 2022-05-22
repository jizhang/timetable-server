const sendJson = require('send-data/json')

function ping(req, res) {
  sendJson(req, res, 'pong')
}

module.exports = {
  'GET /event/ping': ping,
}
