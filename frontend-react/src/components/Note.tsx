import * as dayjs from 'dayjs'
import { useState } from 'react'
import { useQuery, useMutation } from 'react-query'
import { useForm } from 'react-hook-form'
import { NoteApi, type NoteForm } from '~/src/openapi'
import * as styles from './Note.module.css'

const noteApi = new NoteApi()
let saveHandler: NodeJS.Timeout

export default function Note() {
  const [created, setCreated] = useState('')

  const { data } = useQuery('note', () => noteApi.getNoteContent())
  const { mutate, isLoading } = useMutation((values: NoteForm) => noteApi.saveNote(values), {
    onSuccess: (data) => {
      setCreated(dayjs(data.created).format('YYYY-MM-DD HH:mm:ss'))
    },
  })

  const { register, handleSubmit } = useForm()

  function handleChangeContent() {
    clearTimeout(saveHandler)
    saveHandler = setTimeout(() => {
      handleSubmit(handleSaveContent)().catch((error) => {
        alert(`Unexpected error ${String(error)}`)
      })
    }, 5000)
  }

  function handleSaveContent(values: NoteForm) {
    clearTimeout(saveHandler)
    mutate(values)
  }

  return (
    <form onSubmit={handleSubmit(handleSaveContent)}>
      <div className={styles.title}>Note</div>
      <div>
        <textarea
          {...register('content', { onChange: handleChangeContent })}
          className={styles.content}
          defaultValue={data?.content}
        />
      </div>
      <div>
        <input type="submit" value="Save" disabled={isLoading} />
      </div>
      {created && <div>Saved {created}</div>}
    </form>
  )
}
