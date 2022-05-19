const dayjs = require('dayjs')
const sendJson = require('send-data/json')

function getContent(req, res) {
  sendJson(req, res, {
    content: 'test',
  })
}

function save(req, res) {
  const payload = {
    content: req.body.content,
    created: dayjs().toISOString(),
  }
  sendJson(req, res, payload)
}

module.exports = {
  'GET /note/content': getContent,
  'POST /note/save': save,
}
