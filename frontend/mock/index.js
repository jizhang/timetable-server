const sendJson = require('send-data/json')

function ping(req, res) {
  sendJson(req, res, 'pong6')
}

module.exports = {
  'GET /event/ping': ping,
}
