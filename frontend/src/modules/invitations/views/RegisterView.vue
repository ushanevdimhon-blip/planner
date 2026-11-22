<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getOrganizations } from '@/modules/organizations/api'
import { registerByInvite } from '@/modules/invitations/api'

// Токен приглашения берём из ссылки: /invite/:token/register
const route = useRoute()
const token = route.params.token

const form = reactive({
  full_name: '',
  phone: '',
  email: '',
  organization_id: null,
  login: '',
  password: '',
})

const errors = reactive({
  full_name: false,
  email: false,
  organization_id: false,
  login: false,
  password: false,
})

const organizations = ref([])
const loading = ref(true)
const sending = ref(false)
const error = ref('')
const success = ref(false)

onMounted(async () => {
  try {
    organizations.value = await getOrganizations()
  } catch (e) {
    error.value = 'Не удалось загрузить список организаций'
  } finally {
    loading.value = false
  }
})

async function submit() {
  error.value = ''
  success.value = false

  // Сбрасываем подсветку и проверяем каждое поле отдельно
  errors.full_name = !form.full_name
  errors.email = !form.email
  errors.organization_id = !form.organization_id
  errors.login = !form.login
  errors.password = form.password.length < 8

  if (errors.full_name || errors.email || errors.organization_id || errors.login) {
    error.value = 'Заполните выделенные поля'
    return
  }
  if (errors.password) {
    error.value = 'Пароль должен быть не короче 8 символов'
    return
  }

  sending.value = true
  try {
    await registerByInvite(token, { ...form })
    success.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <header class="card-header">Планировщик ПП</header>
  <div class="card">

    <form class="card-body" @submit.prevent="submit">
      <h1>Регистрация по приглашению</h1>

      <label class="field">
        <span>ФИО</span>
        <input v-model="form.full_name" type="text"
          :class="{ invalid: errors.full_name }"
          @input="errors.full_name = false" />
      </label>

      <div class="row">
        <label class="field">
          <span>Телефон</span>
          <input v-model="form.phone" type="tel" placeholder="+7 900 000-00-00" />
        </label>
        <label class="field">
          <span>Почта</span>
          <input v-model="form.email" type="email" placeholder="name@mail.ru"
            :class="{ invalid: errors.email }"
            @input="errors.email = false" />
        </label>
      </div>

      <label class="field">
        <span>Организация</span>
        <select v-model="form.organization_id" :disabled="loading"
          :class="{ invalid: errors.organization_id }"
          @change="errors.organization_id = false">
          <option :value="null" disabled>
            {{ loading ? 'Загрузка...' : 'Выберите организацию из списка' }}
          </option>
          <option v-for="o in organizations" :key="o.id" :value="o.id">
            {{ o.name }}
          </option>
        </select>
      </label>

      <div class="row">
        <label class="field">
          <span>Логин</span>
          <input v-model="form.login" type="text"
            :class="{ invalid: errors.login }"
            @input="errors.login = false" />
        </label>
        <label class="field">
          <span>Пароль</span>
          <input v-model="form.password" type="password" placeholder="••••••••"
            :class="{ invalid: errors.password }"
            @input="errors.password = false" />
        </label>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="ok">Регистрация прошла успешно!</p>

      <button type="submit" :disabled="sending">
        {{ sending ? 'Отправляем...' : 'Зарегистрироваться' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.card-header {
  width: 100%;
  padding: 10px 20px;
  background-color: #5b7fbf;
  color: #000;
  font-size: 16px;
  font-weight: bold;
}

.card {
  width: 50%;
  max-width: 1000px;
  height: 470px;
  margin: 50px auto;
  display: flex;
  border: 1px solid #888;
  background: #121212;
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  padding: 20px 40px 24px;
}

h1 {
  margin: 0 0 2px;
  font-size: 20px;
  color: #ffffff;
}

.row {
  display: flex;
  gap: 12px;
}
.row .field {
  flex: 1;
  min-width: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
}

input,
select {
  width: 100%;
  padding: 8px 10px;
  font-size: 14px;
  color: #eee;
  background: #121212;
  border: 1px solid #888;
}
input::placeholder {
  color: #666;
}

button {
  margin-top: 4px;
  padding: 10px;
  font-size: 15px;
  font-weight: bold;
  color: #ccc;
  background: #1f2937;
  border: 1px solid #5b7fbf;
  border-radius: 8px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.6;
  cursor: default;
}

.error {
  margin: 0;
  color: #e74c3c;
}
.ok {
  margin: 0;
  color: #2ecc71;
}

input.invalid,
select.invalid {
  border-color: #e74c3c;
}
</style>