<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import '@fullcalendar/core/vdom'
import FullCalendar, { CalendarOptions } from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import Note from '@/components/Note.vue'

const modalRef = ref<HTMLElement | null>(null)
let modal: Modal

onMounted(() => {
  if (modalRef.value !== null) {
    modal = new Modal(modalRef.value, {
      backdrop: 'static',
    })
  }
})

function saveEvent() {
  console.log('save')
  modal.hide()
}

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
    modal.show()
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

    <div class="modal fade" ref="modalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">New/Edit Event</h5>
          </div>
          <div class="modal-body">
            ...
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="saveEvent">Save</button>
          </div>
        </div>
      </div>
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
