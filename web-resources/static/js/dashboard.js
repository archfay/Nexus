// Глобальные переменные
let dashboardData = null;
let updateInterval = null;
let uptimeInterval = null;
let botStartTime = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    startAutoUpdate();
    initEventListeners();
});

// Загрузка данных панели
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();
        
        if (data.success) {
            dashboardData = data;
            updateDashboardUI(data);
        } else {
            showNotification('Ошибка загрузки данных', 'error');
            stopUptimeCounter();
            // Обнуляем CPU
            const cpuEl = document.getElementById('cpuUsage');
            if (cpuEl) cpuEl.textContent = '0%';
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        stopUptimeCounter();
        // Обнуляем CPU
        const cpuEl = document.getElementById('cpuUsage');
        if (cpuEl) cpuEl.textContent = '0%';
    }
}

// Демо-данные для разработки
function loadDemoData() {
    const demoData = {
        success: true,
        username: '@demo_user',
        stats: {
            modules_count: 15,
            commands_count: 87,
            uptime: '2h 34m',
            cpu_usage: 12,
            memory_usage: 45,
            messages_processed: 1234
        },
        modules: [
            {
                name: 'Loader',
                description: 'Управление модулями',
                commands: ['loadmod', 'unloadmod', 'dlmod', 'modules'],
                is_core: true
            },
            {
                name: 'Settings',
                description: 'Настройки юзербота',
                commands: ['settings', 'config', 'setprefix'],
                is_core: true
            },
            {
                name: 'Help',
                description: 'Справка по командам',
                commands: ['help'],
                is_core: true
            }
        ]
    };
    
    dashboardData = demoData;
    updateDashboardUI(demoData);
}

// Обновление UI
function updateDashboardUI(data) {
    // Обновляем информацию о пользователе
    if (data.username) {
        const userNameEl = document.getElementById('userName');
        if (userNameEl) {
            userNameEl.textContent = data.username;
        }
    }
    
    // Сохраняем время старта бота для локального обновления uptime
    if (data.bot_start_time) {
        botStartTime = data.bot_start_time;
        startUptimeCounter();
    }
    
    // Обновляем статистику
    if (data.stats) {
        updateStats(data.stats);
    }
    
    // Обновляем список модулей
    if (data.modules) {
        updateModulesList(data.modules);
    }
}

// Обновление статистики
function updateStats(stats) {
    const statsMap = {
        'modulesCount': stats.modules_count,
        'commandsCount': stats.commands_count,
        'uptime': stats.uptime,
        'cpuUsage': `${stats.cpu_usage}%`
    };
    
    for (const [id, value] of Object.entries(statsMap)) {
        const el = document.getElementById(id);
        if (el) {
            // Для uptime просто обновляем без анимации
            if (id === 'uptime') {
                el.textContent = value;
            } else {
                animateValue(el, el.textContent, value);
            }
        }
    }
}

// Анимация изменения значения
function animateValue(element, start, end) {
    // Если значения одинаковые, просто обновляем
    if (start === end) {
        element.textContent = end;
        return;
    }
    
    // Для числовых значений делаем анимацию
    const startNum = parseInt(start) || 0;
    const endNum = parseInt(end) || 0;
    
    if (!isNaN(startNum) && !isNaN(endNum)) {
        const duration = 500;
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(startNum + (endNum - startNum) * progress);
            element.textContent = end.toString().includes('%') ? `${current}%` : current;
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    } else {
        element.textContent = end;
    }
}

// Обновление списка модулей
function updateModulesList(modules) {
    const modulesList = document.getElementById('modulesList');
    if (!modulesList) return;
    
    modulesList.innerHTML = '';
    
    if (!modules || modules.length === 0) {
        modulesList.innerHTML = '<p style="text-align: center; color: #888;">Нет загруженных модулей</p>';
        return;
    }
    
    modules.forEach((module, index) => {
        const card = createModuleCard(module);
        card.style.animationDelay = `${index * 0.05}s`;
        modulesList.appendChild(card);
    });
}

// Создание карточки модуля
function createModuleCard(module) {
    const card = document.createElement('div');
    card.className = 'module-card';
    card.style.animation = 'fadeInUp 0.5s ease-out backwards';
    
    const badgeClass = module.is_core ? 'core' : 'user';
    const badgeText = module.is_core ? 'Core' : 'User';
    
    card.innerHTML = `
        <div class="module-header">
            <h3>${escapeHtml(module.name)}</h3>
            <span class="module-badge ${badgeClass}">${badgeText}</span>
        </div>
        <p class="module-description">${escapeHtml(module.description || 'Нет описания')}</p>
        <div class="module-commands">
            ${module.commands.map(cmd => `<span class="command-tag">.${escapeHtml(cmd)}</span>`).join('')}
        </div>
    `;
    
    return card;
}

// Экранирование HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Перезагрузка бота
async function restartBot() {
    if (!confirm('Вы уверены, что хотите перезагрузить бота?')) return;
    
    showNotification('Перезагрузка бота...', 'info');
    
    try {
        const response = await fetch('/api/bot/restart', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Бот перезагружается...', 'success');
            
            // Ждем 3 секунды и перезагружаем данные
            setTimeout(() => {
                loadDashboardData();
            }, 3000);
        } else {
            showNotification(data.error || 'Ошибка перезагрузки', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Обновление бота
async function updateBot() {
    if (!confirm('Проверить обновления?')) return;
    
    showNotification('Проверка обновлений...', 'info');
    
    try {
        const response = await fetch('/api/bot/update', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.has_updates) {
                showNotification('Обновление установлено! Перезагрузите бота.', 'success');
            } else {
                showNotification('У вас последняя версия', 'info');
            }
        } else {
            showNotification(data.error || 'Ошибка обновления', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Создание бэкапа
async function createBackup() {
    showNotification('Создание бэкапа...', 'info');
    
    try {
        const response = await fetch('/api/bot/backup', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Бэкап создан успешно!', 'success');
            
            if (data.backup_url) {
                // Скачиваем бэкап
                const a = document.createElement('a');
                a.href = data.backup_url;
                a.download = `nexus_backup_${new Date().toISOString().split('T')[0]}.zip`;
                a.click();
            }
        } else {
            showNotification(data.error || 'Ошибка создания бэкапа', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Открыть логи
function openLogs() {
    window.open('/api/bot/logs', '_blank');
}

// Показать модальное окно загрузки модуля
function showLoadModuleModal() {
    const modal = document.getElementById('loadModuleModal');
    if (modal) {
        modal.classList.add('show');
        
        // Фокус на поле URL
        setTimeout(() => {
            const urlInput = document.getElementById('moduleUrl');
            if (urlInput) urlInput.focus();
        }, 300);
    }
}

// Закрыть модальное окно
function closeModal() {
    const modal = document.getElementById('loadModuleModal');
    if (modal) {
        modal.classList.remove('show');
        
        // Очистить поля
        const urlInput = document.getElementById('moduleUrl');
        const fileInput = document.getElementById('moduleFile');
        if (urlInput) urlInput.value = '';
        if (fileInput) fileInput.value = '';
    }
}

// Загрузить модуль
async function loadModule() {
    const urlInput = document.getElementById('moduleUrl');
    const fileInput = document.getElementById('moduleFile');
    
    const url = urlInput ? urlInput.value.trim() : '';
    const file = fileInput ? fileInput.files[0] : null;
    
    if (!url && !file) {
        showNotification('Укажите URL или выберите файл', 'error');
        return;
    }
    
    showNotification('Загрузка модуля...', 'info');
    
    try {
        let response;
        
        if (file) {
            // Загрузка из файла
            const formData = new FormData();
            formData.append('file', file);
            
            response = await fetch('/api/modules/upload', {
                method: 'POST',
                body: formData
            });
        } else {
            // Загрузка по URL
            response = await fetch('/api/modules/load', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
        }
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`Модуль "${data.module_name}" загружен!`, 'success');
            closeModal();
            
            // Обновляем список модулей
            setTimeout(() => loadDashboardData(), 1000);
        } else {
            showNotification(data.error || 'Ошибка загрузки модуля', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Сохранить настройки
async function saveSettings() {
    const settings = {
        prefix: document.getElementById('prefix')?.value || '.',
        api_protection: document.getElementById('apiProtection')?.checked || false,
        auto_update: document.getElementById('autoUpdate')?.checked || false,
        language: document.getElementById('language')?.value || 'ru'
    };
    
    showNotification('Сохранение настроек...', 'info');
    
    try {
        const response = await fetch('/api/settings/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Настройки сохранены!', 'success');
        } else {
            showNotification(data.error || 'Ошибка сохранения', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Показать уведомление
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };
    
    const colors = {
        'success': 'linear-gradient(135deg, #28a745, #20c997)',
        'error': 'linear-gradient(135deg, #dc3545, #c82333)',
        'info': 'linear-gradient(135deg, #17a2b8, #138496)',
        'warning': 'linear-gradient(135deg, #ffc107, #e0a800)'
    };
    
    notification.innerHTML = `
        <span style="font-size: 20px; margin-right: 10px;">${icons[type]}</span>
        <span>${message}</span>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 18px 28px;
        background: ${colors[type]};
        color: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        z-index: 3000;
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        display: flex;
        align-items: center;
        font-weight: 600;
        max-width: 400px;
        backdrop-filter: blur(10px);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        setTimeout(() => notification.remove(), 400);
    }, 4000);
}

// Локальное обновление uptime каждую секунду
function startUptimeCounter() {
    // Останавливаем предыдущий счетчик если есть
    if (uptimeInterval) {
        clearInterval(uptimeInterval);
    }
    
    // Обновляем каждую секунду
    uptimeInterval = setInterval(() => {
        if (botStartTime) {
            const currentTime = Date.now() / 1000;
            const uptimeSeconds = Math.floor(currentTime - botStartTime);
            
            if (uptimeSeconds < 0) return;
            
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            const seconds = uptimeSeconds % 60;
            
            let uptimeStr;
            if (hours > 0) {
                uptimeStr = `${hours}h ${minutes}m`;
            } else if (minutes > 0) {
                uptimeStr = `${minutes}m ${seconds}s`;
            } else {
                uptimeStr = `${seconds}s`;
            }
            
            const uptimeEl = document.getElementById('uptime');
            if (uptimeEl) {
                uptimeEl.textContent = uptimeStr;
            }
        }
    }, 1000);
}

// Остановка счетчика uptime
function stopUptimeCounter() {
    if (uptimeInterval) {
        clearInterval(uptimeInterval);
        uptimeInterval = null;
    }
    botStartTime = null;
    const uptimeEl = document.getElementById('uptime');
    if (uptimeEl) {
        uptimeEl.textContent = '0s';
    }
}

// Автообновление данных
function startAutoUpdate() {
    // Обновляем каждые 5 секунд для более быстрого отклика
    updateInterval = setInterval(() => {
        loadDashboardData();
    }, 5000);
}

// Остановка автообновления
function stopAutoUpdate() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
    stopUptimeCounter();
}

// Инициализация обработчиков событий
function initEventListeners() {
    // Закрытие модального окна по клику вне его
    const modal = document.getElementById('loadModuleModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    // Закрытие модального окна по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

// Очистка при уходе со страницы
window.addEventListener('beforeunload', () => {
    stopAutoUpdate();
});

// Добавляем CSS для анимаций
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
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

console.log('Nexus Dashboard loaded');
