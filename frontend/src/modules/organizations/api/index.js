import { http } from '@/core/http'
import { USE_MOCK } from '@/core/config'
import * as mock from './mock'

// Бэкенд: GET /organizations (публичный)
export const getOrganizations = USE_MOCK ? mock.getOrganizations : () => http.get('/organizations')
