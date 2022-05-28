import dayjs from 'dayjs'
import { MockMethod } from 'vite-plugin-mock'

function getEvenList() {
  const now = dayjs()
  return [
    {
      id: 1,
      title: 'event 1',
      start: now.format('YYYY-MM-DD 09:00:00'),
      end: now.format('YYYY-MM-DD 10:00:00'),
    },
    {
      id: 2,
      title: 'event 2',
      start: now.format('YYYY-MM-DD 10:30:00'),
      end: now.format('YYYY-MM-DD 11:00:00'),
    },
  ]
}

export default [
  {
    url: '/api/event/list',
    response: getEvenList,
  },
] as MockMethod[]
