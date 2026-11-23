import { http } from '@/core/http'
import { USE_MOCK } from '@/core/config'
import * as mock from './mock'

export const registerByInvite = USE_MOCK
  ? mock.registerByInvite
  : (token, data) => http.post(`/invites/${token}/register`, data)
