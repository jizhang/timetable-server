
import { useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import * as styles from './Event.module.css'

async function ping() {
  const response = await fetch('/event/ping')
  return await response.json()
}

export default function() {
  useEffect(() => {
    ping().then(response => {
      console.log(response)
    })
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
