// Particles.js configuration - Enhanced with beautiful effects
particlesJS('particles-js', {
    particles: {
        number: { 
            value: 150, 
            density: { enable: true, value_area: 800 } 
        },
        color: { 
            value: ['#00d4ff', '#ff3366', '#ffcc00', '#667eea', '#f093fb'] 
        },
        shape: { 
            type: ['circle', 'triangle', 'edge', 'polygon'],
            stroke: { width: 0, color: '#000000' },
            polygon: { nb_sides: 6 }
        },
        opacity: { 
            value: 0.7, 
            random: true,
            anim: { 
                enable: true, 
                speed: 1, 
                opacity_min: 0.1, 
                sync: false 
            }
        },
        size: { 
            value: 5, 
            random: true,
            anim: { 
                enable: true, 
                speed: 4, 
                size_min: 0.3, 
                sync: false 
            }
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#00d4ff',
            opacity: 0.6,
            width: 2,
            shadow: {
                enable: true,
                color: '#00d4ff',
                blur: 5
            }
        },
        move: {
            enable: true,
            speed: 3,
            direction: 'none',
            random: true,
            straight: false,
            out_mode: 'bounce',
            bounce: true,
            attract: { 
                enable: true, 
                rotateX: 800, 
                rotateY: 1600 
            }
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: { 
                enable: true, 
                mode: ['grab', 'bubble'] 
            },
            onclick: { 
                enable: true, 
                mode: 'repulse' 
            },
            resize: true
        },
        modes: {
            grab: { 
                distance: 250, 
                line_linked: { 
                    opacity: 1,
                    color: '#ff3366'
                } 
            },
            bubble: { 
                distance: 300, 
                size: 10, 
                duration: 2, 
                opacity: 1,
                speed: 3
            },
            repulse: { 
                distance: 200, 
                duration: 0.4 
            },
            push: { 
                particles_nb: 4 
            },
            remove: { 
                particles_nb: 2 
            }
        }
    },
    retina_detect: true
});

// Smooth scrolling для навигации с улучшенными эффектами
document.querySelectorAll('.sidebar a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Добавляем эффект вспышки с улучшенной анимацией
            target.style.animation = 'none';
            setTimeout(() => {
                target.style.animation = 'highlight 1.5s ease-in-out, scaleIn 0.8s ease-out';
            }, 10);
        }
    });
});

// Подсветка активного раздела при скролле
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.sidebar a');

window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
    
    // Показать/скрыть кнопку "наверх"
    const scrollTop = document.getElementById('scrollTop');
    if (window.pageYOffset > 300) {
        scrollTop.classList.add('visible');
    } else {
        scrollTop.classList.remove('visible');
    }
});

// Кнопка "наверх"
document.getElementById('scrollTop').addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Theme Toggle
let isDark = true;
document.getElementById('themeToggle').addEventListener('click', function() {
    isDark = !isDark;
    document.body.style.transition = 'all 0.3s';
    
    if (isDark) {
        this.innerHTML = '<i class="fas fa-moon"></i>';
        document.documentElement.style.setProperty('--dark', '#0f0f1e');
        document.documentElement.style.setProperty('--darker', '#0a0a14');
        document.documentElement.style.setProperty('--text', '#e0e0e0');
    } else {
        this.innerHTML = '<i class="fas fa-sun"></i>';
        document.documentElement.style.setProperty('--dark', '#f5f5f5');
        document.documentElement.style.setProperty('--darker', '#ffffff');
        document.documentElement.style.setProperty('--text', '#1a1a1a');
    }
});

// Копирование кода по клику с улучшенным дизайном
document.querySelectorAll('.code-block').forEach(block => {
    const button = document.createElement('button');
    button.className = 'copy-btn';
    button.innerHTML = '<i class="fas fa-copy"></i>';
    button.style.cssText = `
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #00d4ff, #ff3366);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 10px 15px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        z-index: 10;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    `;
    
    block.style.position = 'relative';
    block.appendChild(button);
    
    block.addEventListener('mouseenter', () => {
        button.style.opacity = '1';
        button.style.transform = 'translateY(0)';
    });
    
    block.addEventListener('mouseleave', () => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(-10px)';
    });
    
    button.addEventListener('click', () => {
        const code = block.querySelector('code').textContent;
        navigator.clipboard.writeText(code).then(() => {
            button.innerHTML = '<i class="fas fa-check"></i> Скопировано!';
            button.style.background = 'linear-gradient(135deg, #00e676, #00c853)';
            button.style.transform = 'scale(1.1)';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i>';
                button.style.background = 'linear-gradient(135deg, #00d4ff, #ff3366)';
                button.style.transform = 'scale(1)';
            }, 2000);
        });
    });
});

// Анимация появления элементов
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Поиск по документации с улучшенным дизайном
const searchInput = document.createElement('input');
searchInput.type = 'text';
searchInput.placeholder = '🔍 Поиск... (Ctrl+K)';
searchInput.style.cssText = `
    width: 100%;
    padding: 14px 18px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, rgba(21, 27, 61, 0.8), rgba(10, 14, 39, 0.9));
    border: 2px solid rgba(0, 212, 255, 0.3);
    border-radius: 12px;
    color: #e8eaf6;
    font-size: 14px;
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
`;

searchInput.addEventListener('focus', function() {
    this.style.borderColor = '#00d4ff';
    this.style.boxShadow = '0 0 25px rgba(0, 212, 255, 0.6), 0 0 50px rgba(255, 51, 102, 0.3)';
    this.style.transform = 'scale(1.02)';
});

searchInput.addEventListener('blur', function() {
    this.style.borderColor = 'rgba(0, 212, 255, 0.3)';
    this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.3)';
    this.style.transform = 'scale(1)';
});

document.querySelector('.sidebar').insertBefore(searchInput, document.querySelector('.sidebar ul'));

let searchTimeout;
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const searchTerm = e.target.value.toLowerCase();
        const sections = document.querySelectorAll('section');
        let foundCount = 0;
        
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            if (text.includes(searchTerm) || searchTerm === '') {
                section.style.display = 'block';
                foundCount++;
            } else {
                section.style.display = 'none';
            }
        });
        
        // Показываем количество результатов с улучшенной визуализацией
        if (searchTerm && foundCount === 0) {
            searchInput.style.borderColor = '#ff1744';
            searchInput.style.boxShadow = '0 0 25px rgba(255, 23, 68, 0.6)';
        } else if (searchTerm) {
            searchInput.style.borderColor = '#00e676';
            searchInput.style.boxShadow = '0 0 25px rgba(0, 230, 118, 0.6)';
        }
    }, 300);
});

// FAQ аккордеон
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function() {
        const faqItem = this.parentElement;
        const isActive = faqItem.classList.contains('active');
        
        // Закрываем все остальные
        document.querySelectorAll('.faq-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Открываем текущий, если он был закрыт
        if (!isActive) {
            faqItem.classList.add('active');
        }
    });
});

// Анимация чисел в статистике
function animateNumber(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + '+';
        }
    }, 30);
}

// Запускаем анимацию чисел при появлении
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const numbers = entry.target.querySelectorAll('.stat-number');
            numbers.forEach(num => {
                const target = parseInt(num.textContent);
                animateNumber(num, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Добавляем CSS для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes highlight {
        0% { box-shadow: 0 0 0 rgba(0, 212, 255, 0); }
        50% { box-shadow: 0 0 50px rgba(0, 212, 255, 0.8), 0 0 100px rgba(255, 51, 102, 0.4); }
        100% { box-shadow: 0 0 0 rgba(0, 212, 255, 0); }
    }
    
    @keyframes scaleIn {
        0% { transform: scale(0.95); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes slideInRight {
        0% { transform: translateX(100px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        0% { transform: translateX(0); opacity: 1; }
        100% { transform: translateX(100px); opacity: 0; }
    }
    
    @keyframes fadeOut {
        0% { opacity: 1; }
        100% { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Эффект печатающегося текста для заголовка
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Параллакс эффект для hero секции с улучшенной плавностью
let mouseX = 0, mouseY = 0;
let currentX = 0, currentY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 30;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 30;
});

function animateParallax() {
    currentX += (mouseX - currentX) * 0.1;
    currentY += (mouseY - currentY) * 0.1;
    
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translate(${currentX}px, ${currentY}px)`;
    }
    
    requestAnimationFrame(animateParallax);
}

animateParallax();

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K для фокуса на поиске
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
    }
    
    // Escape для очистки поиска
    if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        searchInput.blur();
        document.querySelectorAll('section').forEach(s => s.style.display = 'block');
    }
});

// Показываем подсказку о горячих клавишах с улучшенным дизайном
setTimeout(() => {
    const hint = document.createElement('div');
    hint.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.95), rgba(102, 126, 234, 0.95));
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        font-size: 13px;
        z-index: 999;
        animation: slideInRight 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.5), inset 0 0 20px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 500;
    `;
    hint.innerHTML = '<i class="fas fa-keyboard"></i> Нажмите <strong>Ctrl+K</strong> для поиска';
    document.body.appendChild(hint);
    
    setTimeout(() => {
        hint.style.animation = 'slideOutRight 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        setTimeout(() => hint.remove(), 600);
    }, 4000);
}, 2000);

console.log('%c🚀 Nexus Documentation', 'font-size: 24px; font-weight: bold; background: linear-gradient(90deg, #00d4ff, #ff3366); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');
console.log('%c✨ Loaded successfully with enhanced animations!', 'font-size: 14px; color: #00d4ff;');
console.log('%c💡 Tip: Press Ctrl+K to search', 'font-size: 12px; color: #9fa8da;');


// Кастомный курсор с эффектом следа
const cursor = document.createElement('div');
cursor.className = 'custom-cursor';
cursor.style.cssText = `
    position: fixed;
    width: 20px;
    height: 20px;
    border: 2px solid #00d4ff;
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: all 0.1s ease;
    mix-blend-mode: difference;
`;
document.body.appendChild(cursor);

const cursorDot = document.createElement('div');
cursorDot.className = 'cursor-dot';
cursorDot.style.cssText = `
    position: fixed;
    width: 8px;
    height: 8px;
    background: #ff3366;
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: all 0.05s ease;
`;
document.body.appendChild(cursorDot);

let mouseX = 0, mouseY = 0;
let cursorX = 0, cursorY = 0;
let dotX = 0, dotY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

function animateCursor() {
    cursorX += (mouseX - cursorX) * 0.1;
    cursorY += (mouseY - cursorY) * 0.1;
    dotX += (mouseX - dotX) * 0.15;
    dotY += (mouseY - dotY) * 0.15;
    
    cursor.style.left = cursorX - 10 + 'px';
    cursor.style.top = cursorY - 10 + 'px';
    cursorDot.style.left = dotX - 4 + 'px';
    cursorDot.style.top = dotY - 4 + 'px';
    
    requestAnimationFrame(animateCursor);
}

animateCursor();

// Увеличение курсора при наведении на интерактивные элементы
document.querySelectorAll('a, button, .feature-card, .faq-question').forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursor.style.width = '40px';
        cursor.style.height = '40px';
        cursor.style.borderColor = '#ff3366';
        cursor.style.borderWidth = '3px';
        cursorDot.style.width = '12px';
        cursorDot.style.height = '12px';
        cursorDot.style.background = '#00d4ff';
    });
    
    el.addEventListener('mouseleave', () => {
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.borderColor = '#00d4ff';
        cursor.style.borderWidth = '2px';
        cursorDot.style.width = '8px';
        cursorDot.style.height = '8px';
        cursorDot.style.background = '#ff3366';
    });
});

// Эффект ряби при клике
document.addEventListener('click', (e) => {
    const ripple = document.createElement('div');
    ripple.style.cssText = `
        position: fixed;
        left: ${e.clientX}px;
        top: ${e.clientY}px;
        width: 0;
        height: 0;
        border-radius: 50%;
        border: 2px solid #00d4ff;
        pointer-events: none;
        z-index: 9998;
        animation: rippleEffect 0.8s ease-out;
    `;
    document.body.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 800);
});

// Добавляем CSS для эффекта ряби
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes rippleEffect {
        0% {
            width: 0;
            height: 0;
            opacity: 1;
            margin-left: 0;
            margin-top: 0;
        }
        100% {
            width: 100px;
            height: 100px;
            opacity: 0;
            margin-left: -50px;
            margin-top: -50px;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Эффект магнитного притяжения для кнопок
document.querySelectorAll('.cta-btn, .theme-toggle, .scroll-top').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px) scale(1.05)`;
    });
    
    btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
    });
});

// Параллакс для карточек при движении мыши
document.querySelectorAll('.feature-card, .feature-box').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        
        const rotateX = (y - 0.5) * 20;
        const rotateY = (x - 0.5) * -20;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });
});

// Добавляем эффект свечения при скролле
let lastScrollTop = 0;
window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollDirection = scrollTop > lastScrollTop ? 'down' : 'up';
    lastScrollTop = scrollTop;
    
    // Добавляем эффект свечения к элементам при скролле
    document.querySelectorAll('section').forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.75 && rect.bottom > 0) {
            section.style.filter = 'brightness(1.1)';
        } else {
            section.style.filter = 'brightness(1)';
        }
    });
});

// Добавляем эффект печатающегося текста для заголовков
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    element.style.borderRight = '2px solid #00d4ff';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else {
            setTimeout(() => {
                element.style.borderRight = 'none';
            }, 500);
        }
    }
    type();
}

// Применяем эффект печати к заголовку при загрузке
window.addEventListener('load', () => {
    const heroTitle = document.querySelector('.hero-title, .glitch');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        setTimeout(() => {
            typeWriter(heroTitle, originalText, 80);
        }, 500);
    }
});

// Добавляем эффект частиц при наведении на карточки
document.querySelectorAll('.feature-card, .feature-box').forEach(card => {
    card.addEventListener('mouseenter', function() {
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.style.cssText = `
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: ${['#00d4ff', '#ff3366', '#ffcc00'][Math.floor(Math.random() * 3)]};
                    border-radius: 50%;
                    pointer-events: none;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation: particleFloat 1s ease-out forwards;
                `;
                this.appendChild(particle);
                
                setTimeout(() => particle.remove(), 1000);
            }, i * 100);
        }
    });
});

// CSS для анимации частиц
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes particleFloat {
        0% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
        100% {
            transform: translateY(-50px) scale(0);
            opacity: 0;
        }
    }
`;
document.head.appendChild(particleStyle);

console.log('%c✨ Enhanced animations loaded!', 'font-size: 14px; color: #00d4ff; font-weight: bold;');
