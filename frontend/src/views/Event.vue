<script setup lang="ts">
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

const options = {
  plugins: [timeGridPlugin, interactionPlugin],
  nowIndicator: true,
  selectable: true,
  allDaySlot: false,
  firstDay: 1,
  scrollTime: '08:00:00',
}
</script>

<template>
  <div style="width: 1000px">
    <FullCalendar :options="options" />
  </div>
</template>

<style>
tr {
  height: 30px;
}
</style>
