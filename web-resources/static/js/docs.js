// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    initCodeBlocks();
    initSmoothScroll();
    initSidebarHighlight();
    initSearchFeature();
});

// Инициализация блоков кода
function initCodeBlocks() {
    document.querySelectorAll('.code-block').forEach((block, index) => {
        // Добавляем кнопку копирования
        if (!block.querySelector('.copy-btn')) {
            addCopyButton(block);
        }
        
        // Добавляем номера строк
        addLineNumbers(block);
        
        // Подсветка синтаксиса (базовая)
        highlightSyntax(block);
    });
}

// Добавление кнопки копирования
function addCopyButton(block) {
    const button = document.createElement('button');
    button.className = 'copy-btn';
    button.innerHTML = '📋 Копировать';
    button.title = 'Копировать код';
    
    button.style.cssText = `
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(102, 126, 234, 0.2));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.4);
        color: white;
        padding: 10px 18px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 600;
        opacity: 0;
        transition: all 0.3s;
        z-index: 10;
    `;
    
    block.style.position = 'relative';
    block.appendChild(button);
    
    // Показываем кнопку при наведении
    block.addEventListener('mouseenter', () => {
        button.style.opacity = '1';
    });
    
    block.addEventListener('mouseleave', () => {
        button.style.opacity = '0';
    });
    
    // Копирование кода
    button.addEventListener('click', async () => {
        const code = block.querySelector('pre code').textContent;
        
        try {
            await navigator.clipboard.writeText(code);
            
            button.innerHTML = '✅ Скопировано!';
            button.style.background = 'linear-gradient(135deg, rgba(0, 230, 118, 0.3), rgba(40, 167, 69, 0.3))';
            button.style.borderColor = '#00e676';
            
            setTimeout(() => {
                button.innerHTML = '📋 Копировать';
                button.style.background = 'linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(102, 126, 234, 0.2))';
                button.style.borderColor = 'rgba(0, 212, 255, 0.4)';
            }, 2000);
        } catch (err) {
            button.innerHTML = '❌ Ошибка';
            button.style.background = 'linear-gradient(135deg, rgba(255, 23, 68, 0.3), rgba(220, 53, 69, 0.3))';
            
            setTimeout(() => {
                button.innerHTML = '📋 Копировать';
                button.style.background = 'linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(102, 126, 234, 0.2))';
            }, 2000);
        }
    });
}

// Добавление номеров строк
function addLineNumbers(block) {
    const pre = block.querySelector('pre');
    const code = block.querySelector('code');
    
    if (!pre || !code) return;
    
    const lines = code.textContent.split('\n');
    
    // Создаем контейнер для номеров строк
    const lineNumbers = document.createElement('div');
    lineNumbers.className = 'line-numbers';
    lineNumbers.style.cssText = `
        position: absolute;
        left: 0;
        top: 0;
        padding: 30px 15px;
        color: rgba(255, 255, 255, 0.3);
        font-family: 'Fira Code', 'Consolas', monospace;
        font-size: 15px;
        line-height: 1.7;
        text-align: right;
        user-select: none;
        border-right: 1px solid rgba(0, 212, 255, 0.2);
        background: rgba(0, 0, 0, 0.2);
    `;
    
    lines.forEach((_, index) => {
        const lineNumber = document.createElement('div');
        lineNumber.textContent = index + 1;
        lineNumbers.appendChild(lineNumber);
    });
    
    block.style.position = 'relative';
    block.insertBefore(lineNumbers, pre);
    
    // Добавляем отступ для кода
    pre.style.paddingLeft = '60px';
}

// Базовая подсветка синтаксиса
function highlightSyntax(block) {
    const code = block.querySelector('code');
    if (!code) return;
    
    let html = code.innerHTML;
    
    // Ключевые слова Python
    const keywords = ['def', 'class', 'import', 'from', 'async', 'await', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with', 'as', 'in', 'not', 'and', 'or'];
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b(${keyword})\\b`, 'g');
        html = html.replace(regex, '<span style="color: #c586c0;">$1</span>');
    });
    
    // Строки
    html = html.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '<span style="color: #ce9178;">$&</span>');
    
    // Комментарии
    html = html.replace(/(#.*$)/gm, '<span style="color: #6a9955;">$1</span>');
    
    // Декораторы
    html = html.replace(/(@\w+)/g, '<span style="color: #4ec9b0;">$1</span>');
    
    code.innerHTML = html;
}

// Плавная прокрутка к якорям
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            if (href === '#') return;
            
            e.preventDefault();
            
            const target = document.querySelector(href);
            if (target) {
                const offset = 100; // Отступ от верха
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Обновляем URL
                history.pushState(null, null, href);
            }
        });
    });
}

// Подсветка активного раздела в сайдбаре
function initSidebarHighlight() {
    const sections = document.querySelectorAll('.doc-section');
    const sidebarLinks = document.querySelectorAll('.docs-sidebar a');
    
    if (sections.length === 0 || sidebarLinks.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                
                // Убираем активный класс со всех ссылок
                sidebarLinks.forEach(link => link.classList.remove('active'));
                
                // Добавляем активный класс к текущей ссылке
                const activeLink = document.querySelector(`.docs-sidebar a[href="#${id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, {
        rootMargin: '-100px 0px -80% 0px'
    });
    
    sections.forEach(section => observer.observe(section));
}

// Функция поиска по документации
function initSearchFeature() {
    // Создаем поле поиска
    const searchContainer = document.createElement('div');
    searchContainer.className = 'docs-search';
    searchContainer.style.cssText = `
        position: sticky;
        top: 80px;
        margin-bottom: 30px;
        z-index: 100;
    `;
    
    searchContainer.innerHTML = `
        <input 
            type="text" 
            id="docsSearch" 
            placeholder="🔍 Поиск по документации..."
            style="
                width: 100%;
                padding: 15px 20px;
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 15px;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                font-size: 16px;
                transition: all 0.3s;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            "
        >
        <div id="searchResults" style="
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 10px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 15px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            max-height: 400px;
            overflow-y: auto;
            z-index: 1000;
        "></div>
    `;
    
    const docsContent = document.querySelector('.docs-content');
    if (docsContent) {
        docsContent.insertBefore(searchContainer, docsContent.firstChild);
        
        const searchInput = document.getElementById('docsSearch');
        const searchResults = document.getElementById('searchResults');
        
        // Стили для фокуса
        searchInput.addEventListener('focus', () => {
            searchInput.style.borderColor = 'var(--primary)';
            searchInput.style.boxShadow = '0 0 20px var(--glow)';
        });
        
        searchInput.addEventListener('blur', () => {
            searchInput.style.borderColor = 'rgba(0, 212, 255, 0.3)';
            searchInput.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
            
            // Скрываем результаты с задержкой
            setTimeout(() => {
                searchResults.style.display = 'none';
            }, 200);
        });
        
        // Поиск
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            
            const query = e.target.value.trim().toLowerCase();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query, searchResults);
            }, 300);
        });
    }
}

// Выполнение поиска
function performSearch(query, resultsContainer) {
    const sections = document.querySelectorAll('.doc-section');
    const results = [];
    
    sections.forEach(section => {
        const title = section.querySelector('h1, h2, h3')?.textContent || '';
        const content = section.textContent.toLowerCase();
        
        if (content.includes(query)) {
            const id = section.id || '';
            const snippet = extractSnippet(section.textContent, query);
            
            results.push({
                title: title,
                snippet: snippet,
                id: id
            });
        }
    });
    
    displaySearchResults(results, resultsContainer);
}

// Извлечение фрагмента текста
function extractSnippet(text, query) {
    const index = text.toLowerCase().indexOf(query.toLowerCase());
    if (index === -1) return text.substring(0, 100) + '...';
    
    const start = Math.max(0, index - 50);
    const end = Math.min(text.length, index + query.length + 50);
    
    let snippet = text.substring(start, end);
    if (start > 0) snippet = '...' + snippet;
    if (end < text.length) snippet = snippet + '...';
    
    // Подсвечиваем найденное слово
    const regex = new RegExp(`(${query})`, 'gi');
    snippet = snippet.replace(regex, '<mark style="background: #ffeb3b; padding: 2px 4px; border-radius: 3px;">$1</mark>');
    
    return snippet;
}

// Отображение результатов поиска
function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div style="padding: 20px; text-align: center; color: #888;">Ничего не найдено</div>';
        container.style.display = 'block';
        return;
    }
    
    container.innerHTML = results.map(result => `
        <a href="#${result.id}" style="
            display: block;
            padding: 15px 20px;
            text-decoration: none;
            color: inherit;
            border-bottom: 1px solid rgba(0, 212, 255, 0.1);
            transition: all 0.3s;
        " onmouseover="this.style.background='rgba(0, 212, 255, 0.1)'" onmouseout="this.style.background='transparent'">
            <div style="font-weight: 700; color: var(--primary); margin-bottom: 5px;">${result.title}</div>
            <div style="font-size: 14px; color: #666;">${result.snippet}</div>
        </a>
    `).join('');
    
    container.style.display = 'block';
}

// Добавляем кнопку "Наверх"
function addScrollToTop() {
    const button = document.createElement('button');
    button.innerHTML = '↑';
    button.className = 'scroll-to-top';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 24px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s;
        box-shadow: 0 5px 20px var(--glow);
        z-index: 1000;
    `;
    
    document.body.appendChild(button);
    
    // Показываем кнопку при прокрутке
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            button.style.opacity = '1';
            button.style.visibility = 'visible';
        } else {
            button.style.opacity = '0';
            button.style.visibility = 'hidden';
        }
    });
    
    // Прокрутка наверх
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Эффект при наведении
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'scale(1.1) translateY(-5px)';
        button.style.boxShadow = '0 10px 30px var(--glow)';
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'scale(1) translateY(0)';
        button.style.boxShadow = '0 5px 20px var(--glow)';
    });
}

// Инициализируем кнопку "Наверх"
addScrollToTop();

console.log('Nexus Docs loaded');
