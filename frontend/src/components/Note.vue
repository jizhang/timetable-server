<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'
import { noteApi } from '@/api'

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
    <textarea class="content font-monospace lh-sm" v-model="form.content" @input="handleChangeContent"></textarea>
    <div>
      <button type="submit" class="btn btn-primary btn-sm" :disabled="isLoading">Save</button>
    </div>
    <div v-if="created" class="alert alert-success saved">
      Saved {{ created }}
    </div>
  </form>
</template>

<style scoped>
* {
  --vertical-gap: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  line-height: 30px;
}

.content {
  display: block;
  width: 240px;
  height: 560px;
  margin: var(--vertical-gap) 0;
  font-size: 12px;
}

.saved {
  text-align: center;
  margin-top: var(--vertical-gap);
  padding: 8px;
}
</style>
