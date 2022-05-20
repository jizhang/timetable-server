import * as dayjs from 'dayjs'
import { useState } from 'react'
import { useQuery } from 'react-query'
import { NoteApi } from '~/src/openapi'
import * as styles from './Note.module.css'

const noteApi = new NoteApi()
let saveHandler

export default function() {
  const [content, setContent] = useState<string | null>(null)
  const [created, setCreated] = useState('')

  const { data } = useQuery('note', () => noteApi.getNoteContent())

  function handleChangeContent(event) {
    setContent(event.target.value)
    clearTimeout(saveHandler)
    saveHandler = setTimeout(() => {
      handleSaveContent()
    }, 5000)
  }

  function handleSaveContent() {
    clearTimeout(saveHandler)
    noteApi.saveNote({ content }).then(response => {
      setCreated(dayjs(response.created).format('YYYY-MM-DD HH:mm:ss'))
    })
  }

  return (
    <>
      <div className={styles.title}>Note</div>
      <div>
        <textarea className={styles.content} value={content ?? data?.content} onChange={handleChangeContent} />
      </div>
      <input type="button" value="Save" onClick={handleSaveContent} />
      {created && (
        <div>Saved {created}</div>
      )}
    </>
  )
}
