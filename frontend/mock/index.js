const express = require('express')

const app = express()

app.get('/event/ping', (req, res) => {
  res.json('pong')
})

const server = app.listen(8081, () => {
  console.log('Mock server is listening on port ' + server.address().port)
})
