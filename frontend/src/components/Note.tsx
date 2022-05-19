import * as dayjs from 'dayjs'
import { useState, useEffect } from 'react'
import { NoteApi } from '~/src/openapi'
import * as styles from './Note.module.css'

export default function() {
  const noteApi = new NoteApi()
  const [content, setContent] = useState('')
  const [created, setCreated] = useState('')

  useEffect(() => {
    noteApi.getNoteContent().then(response => {
      setContent(response.content)
    })
  }, [])

  function handleChangeContent(event) {
    setContent(event.target.value)
  }

  function handleSaveContent() {
    noteApi.saveNote({ content }).then(response => {
      setCreated(dayjs(response.created).format('YYYY-MM-DD HH:mm:ss'))
    })
  }

  return (
    <>
      <div className={styles.title}>Note</div>
      <div>
        <textarea className={styles.content} value={content} onChange={handleChangeContent} />
      </div>
      <input type="button" value="Save" onClick={handleSaveContent} />
      {created && (
        <div>Saved {created}</div>
      )}
    </>
  )
}
