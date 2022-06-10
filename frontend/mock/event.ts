import dayjs from 'dayjs'
import { MockMethod } from 'vite-plugin-mock'

function randomInt() {
  return Math.floor(Math.random() * 1_000_000)
}

function getCategories() {
  const categories = [
    {'id': 1, 'title': 'Work', 'color': '#3a87ad'},
    {'id': 2, 'title': 'Meeting', 'color': 'gray'},
    {'id': 3, 'title': 'Self-achievement', 'color': '#ff9c29'},
    {'id': 4, 'title': 'Goofing-around', 'color': 'black'}
  ]

  return { categories }
}

function getEvenList() {
  const now = dayjs()
  const events = [
    {
      id: 1,
      categoryId: 1,
      title: 'abcdefghijklm',
      start: now.format('YYYY-MM-DD 09:00:00'),
      end: now.format('YYYY-MM-DD 10:00:00'),
    },
    {
      id: 2,
      categoryId: 2,
      title: 'nopqrstuvwxyz',
      start: now.format('YYYY-MM-DD 10:30:00'),
      end: now.format('YYYY-MM-DD 11:00:00'),
    },
  ]

  return { events }
}

function saveEvent() {
  return {
    id: randomInt(),
  }
}

function deleteEvent() {
  return {
    id: randomInt(),
  }
}

export default [
  {
    url: '/api/event/categories',
    response: getCategories,
  },
  {
    url: '/api/event/list',
    response: getEvenList,
  },
  {
    url: '/api/event/save',
    method: 'post',
    response: saveEvent,
  },
  {
    url: '/api/event/delete',
    method: 'post',
    response: deleteEvent,
  },
] as MockMethod[]
