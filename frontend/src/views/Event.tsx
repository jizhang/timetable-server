
import { useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { NoteApi } from '~/src/openapi'
import * as styles from './Event.module.css'

export default function() {
  useEffect(() => {
    const note = new NoteApi().saveNote({ content: 'test' })
    console.log(note)
  }, [])

  return (
    <div className={styles.calendar}>
      <FullCalendar
        plugins={[timeGridPlugin, interactionPlugin]}
        nowIndicator={true}
        selectable={true}
        allDaySlot={false}
        firstDay={1}
        scrollTime="08:00:00"
      />
    </div>
  )
}
