const dayjs = require('dayjs')
const sendJson = require('send-data/json')

function save(req, res) {
  const payload = {
    content: req.body.content,
    created: dayjs().toISOString(),
  }
  sendJson(req, res, payload)
}

module.exports = {
  'POST /note/save': save,
}
