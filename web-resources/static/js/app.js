// Состояние авторизации
let isAuthenticated = false;
let dashboardUpdateInterval = null;

// Проверка авторизации при загрузке
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
});

async function checkAuth() {
    const session = getCookie('session');
    
    if (session) {
        // Проверяем валидность сессии
        isAuthenticated = true;
        showMainContent();
        loadDashboard();
        setupNavigation();
        return;
    }
    
    // Проверяем, нужна ли первичная настройка
    try {
        const response = await fetch('/api/auth/check', { method: 'POST' });
        const data = await response.json();
        
        if (data.setup_required) {
            showSetupForm();
        } else {
            showLoginForm();
        }
    } catch (error) {
        console.error('Auth check error:', error);
        showLoginForm();
    }
}

function showSetupForm() {
    document.getElementById('auth-subtitle').textContent = 'Первая настройка';
    document.getElementById('setup-form').style.display = 'block';
    
    document.getElementById('setup-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('setup-username').value;
        const password = document.getElementById('setup-password').value;
        const confirm = document.getElementById('setup-password-confirm').value;
        const errorEl = document.getElementById('setup-error');
        
        if (password !== confirm) {
            errorEl.textContent = 'Пароли не совпадают';
            return;
        }
        
        try {
            const response = await fetch('/api/auth/setup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                setCookie('session', data.session, 30);
                isAuthenticated = true;
                showMainContent();
                loadDashboard();
                setupNavigation();
            } else {
                errorEl.textContent = data.error || 'Ошибка создания аккаунта';
            }
        } catch (error) {
            errorEl.textContent = 'Ошибка соединения';
        }
    });
}

function showLoginForm() {
    document.getElementById('auth-subtitle').textContent = 'Вход в панель';
    document.getElementById('login-form').style.display = 'block';
    
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const errorEl = document.getElementById('login-error');
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                setCookie('session', data.session, 30);
                isAuthenticated = true;
                showMainContent();
                loadDashboard();
                setupNavigation();
            } else {
                errorEl.textContent = data.error || 'Ошибка входа';
            }
        } catch (error) {
            errorEl.textContent = 'Ошибка соединения';
        }
    });
}

function showMainContent() {
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
    // Запускаем автообновление для главной страницы
    const currentPage = document.querySelector('.page.active');
    if (currentPage && currentPage.id === 'page-dashboard') {
        startDashboardUpdates();
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

// Переключение страниц
function showPage(pageName) {
    // Скрыть все страницы
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Показать нужную страницу
    const page = document.getElementById(`page-${pageName}`);
    if (page) {
        page.classList.add('active');
    }
    
    // Обновить активную ссылку
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`.nav-item[data-page="${pageName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
    // Прокрутить наверх
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Управление автообновлением
    if (pageName === 'dashboard') {
        loadDashboard();
        startDashboardUpdates();
    } else {
        stopDashboardUpdates();
    }
}

// Запуск автообновления панели
function startDashboardUpdates() {
    stopDashboardUpdates(); // Остановить предыдущий интервал
    dashboardUpdateInterval = setInterval(() => {
        loadDashboard();
    }, 3000); // Обновление каждые 3 секунды
}

// Остановка автообновления
function stopDashboardUpdates() {
    if (dashboardUpdateInterval) {
        clearInterval(dashboardUpdateInterval);
        dashboardUpdateInterval = null;
    }
}

// Боковое меню
function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

// Обработчики навигации
function setupNavigation() {
    // Клики по навигации
    document.querySelectorAll('.nav-item, .sidebar-link').forEach(item => {
        item.addEventListener('click', (e) => {
            const page = item.getAttribute('data-page');
            if (page) {
                e.preventDefault();
                showPage(page);
            }
        });
    });
}

// Копирование кода
function copyCode(btn) {
    const codeBlock = btn.parentElement;
    const code = codeBlock.querySelector('code').textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        btn.textContent = '✅';
        setTimeout(() => {
            btn.textContent = '📋';
        }, 2000);
    }).catch(() => {
        btn.textContent = '❌';
        setTimeout(() => {
            btn.textContent = '📋';
        }, 2000);
    });
}

// === API функции ===

async function loadDashboard() {
    try {
        const response = await fetch('/api/dashboard/stats', {
            method: 'GET',
            cache: 'no-cache',
            headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStats(data.stats);
            updateModules(data.modules);
            
            // Обновляем время последнего обновления
            const lastUpdate = document.getElementById('last-update');
            if (lastUpdate) {
                const now = new Date();
                lastUpdate.textContent = `Последнее обновление: ${now.toLocaleTimeString('ru-RU')}`;
            }
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function updateStats(stats) {
    if (!stats) return;
    
    const elements = {
        'modules': stats.modules_count || 0,
        'commands': stats.commands_count || 0,
        'uptime': stats.uptime || '0h 0m',
        'cpu': stats.cpu_usage ? `${stats.cpu_usage}%` : '0%'
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const el = document.getElementById(id);
        if (el) {
            // Принудительно обновляем без проверки
            el.style.transition = 'all 0.3s';
            el.style.transform = 'scale(1.1)';
            el.textContent = value;
            setTimeout(() => {
                el.style.transform = 'scale(1)';
            }, 300);
        }
    }
}

function updateModules(modules) {
    if (!modules) return;
    
    const list = document.getElementById('modules-list');
    if (!list) return;
    
    list.innerHTML = '';
    
    if (modules.length === 0) {
        list.innerHTML = '<p style="color: #94a3b8; text-align: center; padding: 20px;">Модули не найдены</p>';
        return;
    }
    
    modules.forEach(mod => {
        const card = document.createElement('div');
        card.className = 'card';
        
        const commandsHtml = mod.commands && mod.commands.length > 0
            ? mod.commands.map(cmd => 
                `<span style="background: rgba(99, 102, 241, 0.2); color: #cbd5e1; padding: 6px 12px; border-radius: 8px; margin-right: 8px; display: inline-block; margin-bottom: 8px; font-family: monospace; border: 1px solid rgba(99, 102, 241, 0.3);">.${cmd}</span>`
              ).join('')
            : '<span style="color: #64748b; font-style: italic;">Нет команд</span>';
        
        card.innerHTML = `
            <h3 style="color: #f1f5f9; margin-bottom: 10px;">${mod.name}</h3>
            <p style="color: #94a3b8; margin-bottom: 15px;">${mod.description || 'Нет описания'}</p>
            <div style="margin-top: 10px;">
                ${commandsHtml}
            </div>
        `;
        list.appendChild(card);
    });
}

async function restartBot() {
    if (!confirm('Перезагрузить бота?')) return;
    
    try {
        const response = await fetch('/api/bot/restart', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showNotification('Бот перезагружается...', 'success');
        } else {
            showNotification(data.error || 'Ошибка', 'error');
        }
    } catch (error) {
        showNotification('Ошибка соединения', 'error');
    }
}

async function updateBot() {
    if (!confirm('Проверить обновления?')) return;
    
    try {
        const response = await fetch('/api/bot/update', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.has_updates ? 'Обновлено!' : 'Последняя версия', 'success');
        } else {
            showNotification(data.error || 'Ошибка', 'error');
        }
    } catch (error) {
        showNotification('Ошибка соединения', 'error');
    }
}

async function createBackup() {
    try {
        const response = await fetch('/api/bot/backup', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showNotification('Бэкап создан!', 'success');
            if (data.backup_url) {
                window.open(data.backup_url, '_blank');
            }
        } else {
            showNotification(data.error || 'Ошибка', 'error');
        }
    } catch (error) {
        showNotification('Ошибка соединения', 'error');
    }
}

function openLogs() {
    window.open('/api/bot/logs', '_blank');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Автообновление каждые 30 секунд (удалено, теперь используется startDashboardUpdates)

// Остановка обновлений при уходе со страницы
window.addEventListener('beforeunload', () => {
    stopDashboardUpdates();
});

// Остановка обновлений при неактивности вкладки
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopDashboardUpdates();
    } else {
        const dashboardPage = document.getElementById('page-dashboard');
        if (dashboardPage && dashboardPage.classList.contains('active')) {
            loadDashboard();
            startDashboardUpdates();
        }
    }
});

console.log('Nexus Web Interface loaded');
