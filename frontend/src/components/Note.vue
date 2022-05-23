<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'
import { NoteApi } from '@/openapi'

const noteApi = new NoteApi()

const isLoading = ref(false)
const created = ref('')
const form = reactive({
  content: '',
})

onMounted(() => {
  noteApi.getNoteContent().then((response) => {
    form.content = response.content || ''
  })
})

let saveHandler: NodeJS.Timeout

function handleChangeContent() {
  clearTimeout(saveHandler)
  saveHandler = setTimeout(() => {
    saveNote()
  }, 5000)
}

function handleSubmit(event: Event) {
  event.preventDefault()
  clearTimeout(saveHandler)
  saveNote()
}

function saveNote() {
  noteApi.saveNote(form).then((response) => {
    created.value = dayjs(response.created).format('YYYY-MM-DD HH:mm:ss')
  })
}
</script>

<template>
  <form @submit="handleSubmit">
    <div class="title">Note</div>
    <div>
      <textarea class="content" v-model="form.content" @input="handleChangeContent"></textarea>
    </div>
    <div>
      <input type="submit" value="Save" :disabled="isLoading" />
    </div>
    <div v-if="created">Saved {{ created }}</div>
  </form>
</template>

<style scoped>
.title {
  font-size: 20px;
  font-weight: bold;
  line-height: 30px;
}

.content {
  width: 240px;
  height: 560px;
}
</style>
