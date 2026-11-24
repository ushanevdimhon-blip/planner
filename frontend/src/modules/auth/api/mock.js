exexport async function loginUser(data) {
    await new Promise((r) => setTimeout(r, 700))

    // В настоящем бэкенде пользователь admin / password123
    if (data.login === 'admin' && data.password === 'password123') {
        // Возвращаем тот же формат, что и Python (access_token)
        return { access_token: 'fake-token-12345' }
    } else {
        throw new Error('Неверный логин или пароль')
    }
}