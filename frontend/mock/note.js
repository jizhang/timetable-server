const dayjs = require('dayjs')
const sendJson = require('send-data/json')

function save(req, res) {
  const now = dayjs().format('YYYY-MM-DD HH:mm:ss')
  sendJson(req, res, `Saved ${now}`)
}

module.exports = {
  'POST /note/save': save,
}
