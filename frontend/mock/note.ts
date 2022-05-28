import dayjs from 'dayjs'
import { MockMethod } from 'vite-plugin-mock'

function getNoteContent() {
  return {
    content: 'test',
  }
}

function saveNote() {
 return {
    content: 'test',
    created: dayjs().toISOString(),
  }
}

export default [
  {
    url: '/api/note/content',
    response: getNoteContent,
  },
  {
    url: '/api/note/save',
    response: saveNote,
  },
] as MockMethod[]
