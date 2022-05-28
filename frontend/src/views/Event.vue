<script setup lang="ts">
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import Note from '@/components/Note.vue'

const options = {
  allDaySlot: false,
  events: '/api/event/list',
  firstDay: 1,
  nowIndicator: true,
  plugins: [timeGridPlugin, interactionPlugin],
  scrollTime: '08:00:00',
  selectable: true,
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
