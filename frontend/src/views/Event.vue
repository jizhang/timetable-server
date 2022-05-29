<script setup lang="ts">
import dayjs from 'dayjs'
import { ref, reactive, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import '@fullcalendar/core/vdom'
import FullCalendar, { CalendarOptions } from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { type EventApi as CalendarEvent } from '@fullcalendar/core'
import Note from '@/components/Note.vue'
import { EventApi, type Category } from '@/openapi'

const formatDate = (date: Date) => dayjs(date).format('YYYY-MM-DD HH:mm:ss')

const eventApi = new EventApi()

const modalRef = ref<HTMLElement | null>(null)
let modal: Modal

onMounted(() => {
  modal = new Modal(modalRef.value!, {
    backdrop: 'static',
  })
})

const defaultEventForm = {
  id: 0,
  categoryId: 1,
  title: '',
  start: '',
  end: '',
}

const eventForm = reactive({
  ...defaultEventForm,
})

const categories = ref<Category[]>([])

onMounted(() => {
  eventApi.getEventCategories().then((response) => {
    categories.value = response.categories || []
  })
})

function saveEvent() {
  console.log(eventForm)
  modal.hide()
}

function updateEventForm(event: CalendarEvent) {
  Object.assign(eventForm, {
    id: event.id,
    categoryId: event.extendedProps.categoryId,
    title: event.title,
    start: formatDate(event.start!),
    end: formatDate(event.end!),
  })
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
    Object.assign(eventForm, {
      ...defaultEventForm,
      start: formatDate(start),
      end: formatDate(end),
    })
    modal.show()
  },

  eventClick({ event }) {
    updateEventForm(event)
    modal.show()
  },

  eventDrop({ event, revert }) {
    updateEventForm(event)
    saveEvent()
  },

  eventResize({ event, revert }) {
    updateEventForm(event)
    saveEvent()
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
            <h5 class="modal-title">{{ eventForm.id ? 'Edit' : 'New' }} Event</h5>
          </div>
          <div class="modal-body">
            <form>
              <div class="row mb-3">
                <label class="col-sm-2 col-form-label">Category:</label>
                <div class="col-sm-10">
                  <select class="form-select" v-model="eventForm.categoryId">
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.title }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <textarea class="form-control" :rows="5" v-model="eventForm.title"></textarea>
              </div>
            </form>
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
