import { MockMethod } from 'vite-plugin-mock'

function ping(req, res) {
  res.setHeader('Content-Type', 'text/plain')
  res.end('pong')
}

export default [
  {
    url: '/api/ping',
    rawResponse: ping,
  },
] as MockMethod[]
