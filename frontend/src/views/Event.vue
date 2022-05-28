<script setup lang="ts">
import '@fullcalendar/core/vdom'
import FullCalendar, { CalendarOptions } from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import Note from '@/components/Note.vue'

const options: CalendarOptions = {
  allDaySlot: false,
  editable: true,
  events: '/api/event/list',
  firstDay: 1,
  nowIndicator: true,
  plugins: [timeGridPlugin, interactionPlugin],
  scrollTime: '08:00:00',
  selectable: true,
  selectOverlap: false,

  select({ start, end }) {
    console.log(start, end)
  },

  eventClick({ event }) {
    console.log(event.title)
  },

  eventDrop({ event, revert }) {
    console.log(event.title, event.start)
  },

  eventResize({ event, revert }) {
    console.log(event.title, event.end)
  },
}
</script>

<template>
  <div>
    <div class="calendar">
      <FullCalendar :options="options" />
    </div>

    <div class="note">
        <Note />
      </div>
  </div>
</template>

<style>
.calendar {
  width: 1000px;
}

.calendar tr {
  height: 30px;
}

.note {
  position: absolute;
  left: 1024px;
  top: 10px;
}
</style>
