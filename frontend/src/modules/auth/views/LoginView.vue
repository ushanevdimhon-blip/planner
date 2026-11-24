<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  login: '',
  password: ''
})

const errors = reactive({
  login: false,
  password: false
})

const error = ref('')
const sending = ref(false)

const submit = async () => {
  error.value = ''
  errors.login = false
  errors.password = false

  // Проверка на пустые поля и длину пароля
  if (!form.login) {
    errors.login = true
  }

  if (!form.password) {
    errors.password = true
  } else if (form.password.length < 8) {
    errors.password = true
    error.value = 'Пароль должен содержать минимум 8 символов'
  }

  if (errors.login || errors.password) {
    return
  }

  sending.value = true

  try {
    // --- ЗАГЛУШКА (МОК) ПРЯМО ЗДЕСЬ ---
    await new Promise((r) => setTimeout(r, 700))

    if (form.login === 'admin' && form.password === 'password123') {
      localStorage.setItem('token', 'fake-token-12345')
      router.push('/') 
    } else {
      throw new Error('Неверный логин или пароль')
    }
    // ----------------------------------
  } catch (err) {
    error.value = err.message || 'Ошибка подключения к серверу'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <header class="card-header">Планировщик ПП</header>
  <div class="card">

    <form class="card-body" @submit.prevent="submit">
      <h1>Вход в систему</h1>

      <!-- Поле Логин -->
      <label class="field">
        <span>Логин</span>
        <input v-model="form.login" type="text" placeholder="Введите логин"
          :class="{ invalid: errors.login }"
          @input="errors.login = false" />
      </label>

      <!-- Поле Пароль -->
      <label class="field">
        <span>Пароль</span>
        <input v-model="form.password" type="password" placeholder="••••••••"
          :class="{ invalid: errors.password }"
          @input="errors.password = false" />
      </label>

      <!-- Вывод ошибок -->
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Кнопка Войти -->
      <button type="submit" :disabled="sending">
        {{ sending ? 'Входим...' : 'Войти' }}
      </button>

      <!-- Ссылка на регистрацию (взято из ТЗ) -->
      <div class="register-link">
        Нет аккаунта? 
        <router-link to="/invite/test-token/register">Зарегистрироваться</router-link>
      </div>

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
  box-sizing: border-box;
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

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
}

input {
  width: 100%;
  padding: 8px 10px;
  font-size: 14px;
  color: #eee;
  background: #121212;
  border: 1px solid #888;
  box-sizing: border-box;
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
  font-size: 13px;
}

input.invalid {
  border-color: #e74c3c;
}

.register-link {
  text-align: center;
  font-size: 13px;
  color: #888;
  margin-top: 10px;
}

.register-link a {
  color: #5b7fbf;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>