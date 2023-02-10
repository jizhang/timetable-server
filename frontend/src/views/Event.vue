<script setup lang="ts">
import dayjs from 'dayjs'
import debounce from 'just-debounce-it'
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { Modal } from 'bootstrap'
import '@fullcalendar/core/vdom'
import FullCalendar, { CalendarOptions } from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { CalendarApi, type FormatterInput } from '@fullcalendar/core'
import type { EventApi as CalendarEvent } from '@fullcalendar/core'
import type { Category } from '@/openapi'
import { commonApi, eventApi } from '@/api'
import Note from '@/components/Note.vue'

// Utilities
function formatDate(date: Date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

function calculateCalendarHeight() {
  return window.innerHeight - 50
}

const timeFormat: FormatterInput = {
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
}

// Calendar
const options: CalendarOptions = {
  allDaySlot: false,
  editable: true,
  eventTimeFormat: timeFormat,
  firstDay: 1,
  height: calculateCalendarHeight(),
  nowIndicator: true,
  plugins: [timeGridPlugin, interactionPlugin],
  scrollTime: '08:00:00',
  selectable: true,
  selectOverlap: false,
  slotLabelFormat: timeFormat,

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

  eventDrop({ event }) {
    updateEventForm(event)
    saveEvent()
  },

  eventResize({ event }) {
    updateEventForm(event)
    saveEvent()
  },

  eventsSet(events) {
    updateCategoryDurations(events)
  },
}

const categories = ref<Category[]>([])
const calendarRef = ref<InstanceType<typeof FullCalendar> | null>(null)
let calendarApi: CalendarApi

const handleResizeWindow = debounce(() => {
  calendarApi.setOption('height', calculateCalendarHeight())
}, 200)

onMounted(() => {
  if (!calendarRef.value) {
    return
  }
  calendarApi = calendarRef.value.getApi()

  // TODO Pinia
  eventApi.getEventCategories().then((response) => {
    categories.value = response.categories || []
    calendarApi.addEventSource(({start, end}) => {
      return getEvents(start, end)
    })
  })

  window.addEventListener('resize', handleResizeWindow)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResizeWindow)
})

function getCategoryColor(categoryId: number) {
  for (const category of categories.value) {
    if (category.id === categoryId) {
      return category.color
    }
  }
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
      color: getCategoryColor(value.categoryId),
    }
  })
}

// Event
let modal: Modal
function saveModalRef(el: HTMLElement | null) {
  if (el !== null) {
    modal = new Modal(el, { backdrop: 'static' })
  }
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

function saveEvent() {
  eventApi.saveEvent(eventForm).then((response) => {
    // TODO Event form may change during request.
    if (!eventForm.id) {
      calendarApi.addEvent({
        ...eventForm,
        id: String(response.id),
        color: getCategoryColor(eventForm.categoryId),
      }, true)
    } else {
      const event = calendarApi.getEventById(String(eventForm.id))
      event?.setProp('title', eventForm.title)
      event?.setProp('color', getCategoryColor(eventForm.categoryId))
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

function handleDeleteEvent() {
  if (confirm('Are you sure?')) {
    eventApi.deleteEvent({ id: eventForm.id }).then(() => {
      const event = calendarApi.getEventById(String(eventForm.id)) // TODO Use response.id
      event?.remove()
      modal.hide()
    })
  }
}

onMounted(() => {
  const pingHandler = setInterval(() => {
    commonApi.ping().catch(() => {
      clearInterval(pingHandler)
      if (confirm('Ping error, reload?')) {
        location.reload()
      }
    })
  }, 30_000)
})

const categoryDurations = ref<{
  title: string
  duration: string
}[]>([])

function updateCategoryDurations(events: CalendarEvent[]) {
  const durations: Record<string, number> = {}

  for (const event of events) {
    const start = dayjs(event.start)
    if (!start.isSame(dayjs(), 'day')) {
      continue
    }

    const end = dayjs(event.end)
    const minutes = end.diff(start, 'minutes')
    const key = String(event.extendedProps.categoryId)
    if (!(key in durations)) {
      durations[key] = 0
    }
    durations[key] += minutes
  }

  categoryDurations.value = categories.value.map((category) => {
    const key = String(category.id)
    let duration: string
    if (key in durations) {
      duration = (durations[key] / 60) + 'h'
    } else {
      duration = '-'
    }
    return {
      title: String(category.title),
      duration,
    }
  })
}
</script>

<template>
  <div>
    <div class="calendar">
      <FullCalendar :options="options" ref="calendarRef" />
    </div>

    <div class="note">
      <Note />

      <div style="margin-top: 10px;">
        <ul class="list-group">
          <li v-for="item in categoryDurations" :key="item.title" class="list-group-item d-flex justify-content-between align-items-center">
            {{ item.title }}
            <span>{{ item.duration }}</span>
          </li>
        </ul>
      </div>
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

.calendar .fc-col-header-cell a {
  color: inherit;
  text-decoration: inherit;
}

.calendar .fc-timegrid-slot {
  height: 30px;
}

.calendar .fc-timegrid-event {
  font-size: 12px;
  line-height: 100%;
}

.calendar .fc-event-title {
  overflow: visible;
}

.note {
  position: absolute;
  left: 1024px;
  top: 10px;
}
</style>
