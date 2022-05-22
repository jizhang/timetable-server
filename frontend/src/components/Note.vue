<script setup lang="ts">
import { ref, reactive } from 'vue'
import dayjs from 'dayjs'
import { NoteApi } from '@/openapi'

const noteApi = new NoteApi()

const isLoading = ref(false)
const created = ref('')
const form = reactive({
  content: '',
})

function handleSubmit(event) {
  event.preventDefault()
  noteApi.saveNote(form).then((response) => {
    created.value = dayjs(response.created).format('YYYY-MM-DD HH:mm:ss')
  })
}
</script>

<template>
  <form @submit="handleSubmit">
    <div class="title">Note</div>
    <div>
      <textarea class="content" v-model="form.content"></textarea>
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
