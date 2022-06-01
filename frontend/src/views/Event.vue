<script setup lang="ts">
import dayjs from 'dayjs'
import { ref, reactive, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import '@fullcalendar/core/vdom'
import FullCalendar, { CalendarOptions } from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { CalendarApi, EventApi as CalendarEvent } from '@fullcalendar/core'
import { EventApi, type Category } from '@/openapi'
import Note from '@/components/Note.vue'

const eventApi = new EventApi()

function formatDate(date: Date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

let modal: Modal
function saveModalRef(el: HTMLElement) {
  modal = new Modal(el, { backdrop: 'static' })
}

let calendarApi: CalendarApi
function saveCalendarRef(el: InstanceType<typeof FullCalendar>) {
  calendarApi = el.getApi()
}

const options: CalendarOptions = {
  allDaySlot: false,
  editable: true,
  firstDay: 1,
  nowIndicator: true,
  plugins: [timeGridPlugin, interactionPlugin],
  scrollTime: '08:00:00',
  selectable: true,
  selectOverlap: false,

  events({ start, end }) {
    return getEvents(start, end)
  },

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

const defaultEventForm = {
  id: 0, // TODO number | null
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
  // TODO Pinia
  eventApi.getEventCategories().then((response) => {
    categories.value = response.categories || []
  })
})

function saveEvent() {
  eventApi.saveEvent(eventForm).then((response) => {
    // TODO Event form may change during request.
    if (!eventForm.id) {
      calendarApi.addEvent({
        ...eventForm,
        id: String(response.id),
      })
    } else {
      const event = calendarApi.getEventById(String(eventForm.id))
      event?.setProp('title', eventForm.title)
      event?.setExtendedProp('categoryId', eventForm.categoryId)
    }
    modal.hide()
  })
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

async function getEvents(start: Date, end: Date) {
  const response = await eventApi.getEventList({ start, end })
  if (!response.events) {
    return []
  }
  return response.events.map((value) => {
    return {
      id: String(value.id),
      categoryId: value.categoryId,
      title: value.title,
      start: value.start,
      end: value.end,
    }
  })
}

function handleDeleteEvent() {
  if (confirm('Are you sure?')) {
    eventApi.deleteEvent({ id: eventForm.id }).then(() => {
      const event = calendarApi.getEventById(String(eventForm.id)) // TODO Use response.id
      event?.remove()
      modal.hide()
    })
  }
}
</script>

<template>
  <div>
    <div class="calendar">
      <FullCalendar :options="options" :ref="saveCalendarRef" />
    </div>

    <div class="note">
      <Note />
    </div>

    <div class="modal" :ref="saveModalRef">
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
            <button v-if="eventForm.id" class="btn btn-danger" @click="handleDeleteEvent">Delete</button>
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
