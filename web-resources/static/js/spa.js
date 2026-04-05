// Управление вкладками
let currentTab = 'home';

// Показать вкладку
function showTab(tabName) {
    // Скрыть все вкладки
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Показать нужную вкладку
    const tab = document.getElementById(`tab-${tabName}`);
    if (tab) {
        tab.classList.add('active');
        currentTab = tabName;
    }
    
    // Обновить активную ссылку в навигации
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`.nav-link[href="#${tabName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
    // Прокрутить наверх
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Загрузить данные для вкладки
    loadTabData(tabName);
}

// Загрузка данных для вкладки
async function loadTabData(tabName) {
    switch(tabName) {
        case 'dashboard':
            await loadDashboardData();
            break;
        case 'docs':
            initDocsFeatures();
            break;
        case 'home':
            checkAuthStatus();
            break;
    }
}

// Боковое меню
function toggleSidebar() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
}

// История браузера
window.addEventListener('popstate', (e) => {
    const hash = window.location.hash.slice(1) || 'home';
    showTab(hash);
});

// Обработка хэша при загрузке
window.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash.slice(1) || 'home';
    showTab(hash);
});

// Обновление хэша при переключении вкладок
const originalShowTab = showTab;
showTab = function(tabName) {
    window.location.hash = tabName;
    originalShowTab(tabName);
};

// ===== ФУНКЦИИ АВТОРИЗАЦИИ =====

let authData = {
    api_id: '',
    api_hash: '',
    phone: '',
    code: '',
    password: '',
    bot_username: ''
};

function showStep(stepNumber) {
    document.querySelectorAll('.auth-step').forEach(step => {
        step.classList.remove('active');
    });
    
    const step = document.getElementById(`step${stepNumber}`);
    if (step) {
        step.classList.add('active');
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} show`;
    alertDiv.textContent = message;
    
    const authCard = document.querySelector('.auth-step.active .auth-card');
    if (authCard) {
        authCard.insertBefore(alertDiv, authCard.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

async function handlePhoneSubmit(event) {
    event.preventDefault();
    const phone = document.getElementById('phone').value;
    authData.phone = phone;
    
    try {
        const response = await fetch('/api/auth/send_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone: phone })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Код отправлен в Telegram', 'success');
            setTimeout(() => showStep(3), 1000);
        } else {
            showAlert(data.error || 'Ошибка отправки кода', 'error');
        }
    } catch (error) {
        showAlert('Ошибка соединения с сервером', 'error');
    }
    
    return false;
}

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

function updateSuccessInfo(data) {
    if (data.prefix) {
        const prefixEl = document.getElementById('prefix');
        if (prefixEl) prefixEl.textContent = data.prefix;
    }
    if (data.modules_count) {
        const modulesEl = document.getElementById('modules_count');
        if (modulesEl) modulesEl.textContent = data.modules_count;
    }
}

// ===== ФУНКЦИИ ПАНЕЛИ УПРАВЛЕНИЯ =====

async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();
        
        if (data.success) {
            updateDashboardStats(data);
            updateModulesList(data.modules);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateDashboardStats(data) {
    if (data.user) {
        const userNameEl = document.getElementById('userName');
        if (userNameEl) userNameEl.textContent = `@${data.user.username}`;
    }
    
    if (data.stats) {
        const elements = {
            'modulesCount': data.stats.modules_count,
            'commandsCount': data.stats.commands_count,
            'uptime': data.stats.uptime,
            'cpuUsage': `${data.stats.cpu_usage}%`
        };
        
        for (const [id, value] of Object.entries(elements)) {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        }
    }
}

function updateModulesList(modules) {
    if (!modules) return;
    
    const modulesList = document.getElementById('modulesList');
    if (!modulesList) return;
    
    modulesList.innerHTML = '';
    
    modules.forEach(module => {
        const card = createModuleCard(module);
        modulesList.appendChild(card);
    });
}

function createModuleCard(module) {
    const card = document.createElement('div');
    card.className = 'module-card';
    
    const badgeClass = module.is_core ? 'core' : 'user';
    const badgeText = module.is_core ? 'Core' : 'User';
    
    card.innerHTML = `
        <div class="module-header">
            <h3>${module.name}</h3>
            <span class="module-badge ${badgeClass}">${badgeText}</span>
        </div>
        <p class="module-description">${module.description || 'Нет описания'}</p>
        <div class="module-commands">
            ${module.commands.map(cmd => `<span class="command-tag">.${cmd}</span>`).join('')}
        </div>
    `;
    
    return card;
}

async function restartBot() {
    if (!confirm('Вы уверены, что хотите перезагрузить бота?')) return;
    
    try {
        const response = await fetch('/api/bot/restart', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showNotification('Бот перезагружается...', 'success');
        } else {
            showNotification(data.error || 'Ошибка перезагрузки', 'error');
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
            if (data.has_updates) {
                showNotification('Обновление установлено!', 'success');
            } else {
                showNotification('У вас последняя версия', 'info');
            }
        } else {
            showNotification(data.error || 'Ошибка обновления', 'error');
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
            showNotification('Бэкап создан успешно!', 'success');
            if (data.backup_url) {
                window.open(data.backup_url, '_blank');
            }
        } else {
            showNotification(data.error || 'Ошибка создания бэкапа', 'error');
        }
    } catch (error) {
        showNotification('Ошибка соединения', 'error');
    }
}

function openLogs() {
    window.open('/api/bot/logs', '_blank');
}

function showLoadModuleModal() {
    // TODO: Реализовать модальное окно
    alert('Функция загрузки модулей в разработке');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 3000;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ===== ФУНКЦИИ ДОКУМЕНТАЦИИ =====

function initDocsFeatures() {
    // Копирование кода
    document.querySelectorAll('.code-block').forEach(block => {
        if (block.querySelector('.copy-btn')) return;
        
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerHTML = '📋';
        button.title = 'Копировать код';
        
        button.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            opacity: 0;
            transition: all 0.3s;
        `;
        
        block.style.position = 'relative';
        block.appendChild(button);
        
        block.addEventListener('mouseenter', () => button.style.opacity = '1');
        block.addEventListener('mouseleave', () => button.style.opacity = '0');
        
        button.addEventListener('click', async () => {
            const code = block.querySelector('pre code').textContent;
            
            try {
                await navigator.clipboard.writeText(code);
                button.innerHTML = '✅';
                button.style.background = 'rgba(40, 167, 69, 0.8)';
                
                setTimeout(() => {
                    button.innerHTML = '📋';
                    button.style.background = 'rgba(255, 255, 255, 0.1)';
                }, 2000);
            } catch (err) {
                button.innerHTML = '❌';
                setTimeout(() => button.innerHTML = '📋', 2000);
            }
        });
    });
}

// Автообновление данных панели каждые 30 секунд
setInterval(() => {
    if (currentTab === 'dashboard') {
        loadDashboardData();
    }
}, 30000);

// Анимации для уведомлений
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

console.log('Nexus SPA loaded');
