// Данные авторизации
let authData = {
    api_id: '',
    api_hash: '',
    phone: '',
    code: '',
    password: '',
    bot_username: ''
};

// Текущий шаг
let currentStep = 1;

// Показать шаг
function showStep(stepNumber) {
    // Скрыть все шаги
    document.querySelectorAll('.auth-step').forEach(step => {
        step.classList.remove('active');
    });
    
    // Показать нужный шаг
    const step = document.getElementById(`step${stepNumber}`);
    if (step) {
        step.classList.add('active');
        currentStep = stepNumber;
        
        // Фокус на первое поле ввода
        setTimeout(() => {
            const firstInput = step.querySelector('input');
            if (firstInput) firstInput.focus();
        }, 300);
    }
}

// Показать уведомление
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} show`;
    alertDiv.innerHTML = `
        <span>${getAlertIcon(type)}</span>
        <span>${message}</span>
    `;
    
    const authCard = document.querySelector('.auth-step.active .auth-card');
    if (authCard) {
        // Удалить предыдущие алерты
        authCard.querySelectorAll('.alert').forEach(alert => alert.remove());
        
        authCard.insertBefore(alertDiv, authCard.firstChild);
        
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }
}

function getAlertIcon(type) {
    const icons = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };
    return icons[type] || icons['info'];
}

// Валидация номера телефона
function validatePhone(phone) {
    // Удаляем все кроме цифр и +
    phone = phone.replace(/[^\d+]/g, '');
    
    // Проверяем формат
    if (!phone.startsWith('+')) {
        return { valid: false, message: 'Номер должен начинаться с +' };
    }
    
    if (phone.length < 10) {
        return { valid: false, message: 'Номер слишком короткий' };
    }
    
    if (phone.length > 15) {
        return { valid: false, message: 'Номер слишком длинный' };
    }
    
    return { valid: true, phone: phone };
}

// Обработка отправки номера телефона
async function handlePhoneSubmit(event) {
    event.preventDefault();
    
    const phoneInput = document.getElementById('phone');
    const phone = phoneInput.value.trim();
    
    // Валидация
    const validation = validatePhone(phone);
    if (!validation.valid) {
        showAlert(validation.message, 'error');
        phoneInput.focus();
        return false;
    }
    
    authData.phone = validation.phone;
    
    // Показать загрузку
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Отправка...';
    submitBtn.disabled = true;
    
    try {
        // Используем существующий endpoint /send_tg_code
        const response = await fetch('/send_tg_code', {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: validation.phone
        });
        
        if (response.status === 200 || response.ok) {
            showAlert('Код отправлен в Telegram!', 'success');
            setTimeout(() => showStep(3), 1500);
        } else if (response.status === 429) {
            const text = await response.text();
            showAlert(text || 'Слишком много попыток', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        } else {
            const text = await response.text();
            showAlert(text || 'Ошибка отправки кода', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Ошибка соединения с сервером', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
    
    return false;
}

// Обработка отправки кода
async function handleCodeSubmit(event) {
    event.preventDefault();
    
    const codeInput = document.getElementById('code');
    const code = codeInput.value.trim();
    
    if (code.length < 5) {
        showAlert('Введите корректный код', 'error');
        codeInput.focus();
        return false;
    }
    
    authData.code = code;
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Проверка...';
    submitBtn.disabled = true;
    
    try {
        // Используем существующий endpoint /tg_code
        const response = await fetch('/tg_code', {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: `${code}\n${authData.phone}\n`
        });
        
        if (response.status === 200) {
            showAlert('Авторизация успешна!', 'success');
            createConfetti();
            // Перенаправляем на dashboard через 2 секунды
            setTimeout(() => {
                window.location.href = '/pages/dashboard.html';
            }, 2000);
        } else if (response.status === 401) {
            showAlert('Требуется пароль 2FA', 'info');
            setTimeout(() => showStep(4), 1500);
        } else if (response.status === 403) {
            showAlert('Неверный код', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        } else if (response.status === 404) {
            showAlert('Код истек', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        } else {
            const text = await response.text();
            showAlert(text || 'Ошибка проверки кода', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Ошибка соединения с сервером', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
    
    return false;
}

// Обработка отправки 2FA пароля
async function handle2FASubmit(event) {
    event.preventDefault();
    
    const passwordInput = document.getElementById('password2fa');
    const password = passwordInput.value;
    
    if (!password) {
        showAlert('Введите пароль', 'error');
        passwordInput.focus();
        return false;
    }
    
    authData.password = password;
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Вход...';
    submitBtn.disabled = true;
    
    try {
        // Используем существующий endpoint /tg_code с паролем
        const response = await fetch('/tg_code', {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: `${authData.code}\n${authData.phone}\n${password}`
        });
        
        if (response.status === 200) {
            showAlert('Авторизация успешна!', 'success');
            createConfetti();
            // Перенаправляем на dashboard через 2 секунды
            setTimeout(() => {
                window.location.href = '/pages/dashboard.html';
            }, 2000);
        } else if (response.status === 403) {
            showAlert('Неверный пароль', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        } else {
            const text = await response.text();
            showAlert(text || 'Ошибка авторизации', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Ошибка соединения с сервером', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
    
    return false;
}

// Обработка отправки API credentials
async function handleApiSubmit(event) {
    event.preventDefault();
    
    const apiIdInput = document.getElementById('api_id');
    const apiHashInput = document.getElementById('api_hash');
    
    const apiId = apiIdInput.value.trim();
    const apiHash = apiHashInput.value.trim();
    
    if (!apiId || !apiHash) {
        showAlert('Заполните все поля', 'error');
        return false;
    }
    
    if (!/^\d+$/.test(apiId)) {
        showAlert('API ID должен содержать только цифры', 'error');
        apiIdInput.focus();
        return false;
    }
    
    if (apiHash.length !== 32) {
        showAlert('API Hash должен содержать 32 символа', 'error');
        apiHashInput.focus();
        return false;
    }
    
    authData.api_id = apiId;
    authData.api_hash = apiHash;
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Проверка...';
    submitBtn.disabled = true;
    
    try {
        // Используем существующий endpoint /set_api
        const response = await fetch('/set_api', {
            method: 'PUT',
            headers: { 'Content-Type': 'text/plain' },
            body: apiHash + apiId
        });
        
        if (response.ok) {
            showAlert('Credentials сохранены!', 'success');
            setTimeout(() => showStep(2), 1500);
        } else {
            const text = await response.text();
            showAlert(text || 'Неверные credentials', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Ошибка соединения с сервером', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
    
    return false;
}

// Обработка отправки номера при регистрации
async function handleRegPhoneSubmit(event) {
    event.preventDefault();
    
    const phoneInput = document.getElementById('reg_phone');
    const botUsernameInput = document.getElementById('bot_username');
    
    const phone = phoneInput.value.trim();
    const botUsername = botUsernameInput.value.trim();
    
    const validation = validatePhone(phone);
    if (!validation.valid) {
        showAlert(validation.message, 'error');
        phoneInput.focus();
        return false;
    }
    
    authData.phone = validation.phone;
    authData.bot_username = botUsername;
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Отправка...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                api_id: authData.api_id,
                api_hash: authData.api_hash,
                phone: validation.phone,
                bot_username: botUsername
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Код отправлен в Telegram!', 'success');
            setTimeout(() => showStep(3), 1500);
        } else {
            showAlert(data.error || 'Ошибка регистрации', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Ошибка соединения с сервером', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
    
    return false;
}

// Обновление информации на странице успеха
function updateSuccessInfo(data) {
    if (data.prefix) {
        const prefixEl = document.getElementById('prefix');
        if (prefixEl) prefixEl.textContent = data.prefix;
    }
    
    if (data.modules_count !== undefined) {
        const modulesEl = document.getElementById('modules_count');
        if (modulesEl) modulesEl.textContent = data.modules_count;
    }
    
    // Анимация конфетти
    createConfetti();
}

// Проверка статуса авторизации при загрузке
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        
        if (data.authenticated) {
            showStep(7);
            updateSuccessInfo(data);
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

// Анимация конфетти
function createConfetti() {
    const colors = ['#00d4ff', '#ff3366', '#ffcc00', '#667eea'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                top: -10px;
                left: ${Math.random() * 100}%;
                opacity: 1;
                border-radius: 50%;
                z-index: 9999;
                pointer-events: none;
                animation: confettiFall ${2 + Math.random() * 2}s linear forwards;
            `;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 4000);
        }, i * 30);
    }
}

// Добавляем CSS для анимации конфетти
const style = document.createElement('style');
style.textContent = `
    @keyframes confettiFall {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Автоформатирование номера телефона
document.addEventListener('DOMContentLoaded', () => {
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^\d+]/g, '');
            
            if (value && !value.startsWith('+')) {
                value = '+' + value;
            }
            
            e.target.value = value;
        });
    });
    
    // Проверка авторизации
    checkAuthStatus();
});

// Обработка Enter для перехода к следующему полю
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const activeElement = document.activeElement;
        
        if (activeElement.tagName === 'INPUT' && activeElement.type !== 'submit') {
            const form = activeElement.closest('form');
            if (form) {
                const inputs = Array.from(form.querySelectorAll('input:not([type="submit"])'));
                const currentIndex = inputs.indexOf(activeElement);
                
                if (currentIndex < inputs.length - 1) {
                    e.preventDefault();
                    inputs[currentIndex + 1].focus();
                }
            }
        }
    }
});

console.log('Nexus Auth loaded');
