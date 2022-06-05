import { Configuration, CommonApi, EventApi, NoteApi } from '@/openapi'

const conf = new Configuration({
  basePath: '',
})

export const commonApi = new CommonApi(conf)
export const eventApi = new EventApi(conf)
export const noteApi = new NoteApi(conf)
