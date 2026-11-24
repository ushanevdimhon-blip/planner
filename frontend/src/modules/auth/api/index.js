import { http } from '@/core/http'
import { USE_MOCK } from '@/core/config'
import * as mock from './mock'

export const loginUser = USE_MOCK ?
    mock.loginUser :
    (data) => http.post('/auth/login', data)