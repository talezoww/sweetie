// Основной JavaScript файл для Sweetie

document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    initMobileMenu();
    
    // Автозакрытие флеш сообщений
    initFlashMessages();
    
    // Плавная прокрутка
    initSmoothScroll();
    
    // Анимации при скролле
    initScrollAnimations();
    
    // Валидация форм
    initFormValidation();
    
    // Предварительный просмотр изображений
    initImagePreview();
    
    // Инициализация других компонентов
    initComponents();
});

// Мобильное меню
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Закрытие меню при клике на ссылку
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

// Флеш сообщения
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
        
        // Закрытие по клику
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
    });
}

// Плавная прокрутка
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Анимации при скролле
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Анимация для карточек
    document.querySelectorAll('.recipe-card, .category-card, .feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Валидация форм
function initFormValidation() {
    // Валидация email
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Валидация пароля
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            validatePassword(this);
        });
    });
    
    // Валидация формы регистрации
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = this.querySelector('input[name="password"]');
            const confirmPassword = this.querySelector('input[name="confirm_password"]');
            
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                e.preventDefault();
                showError('Пароли не совпадают');
                return false;
            }
        });
    }
}

// Валидация email
function validateEmail(input) {
    const email = input.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        showFieldError(input, 'Некорректный email адрес');
        return false;
    } else {
        clearFieldError(input);
        return true;
    }
}

// Валидация пароля
function validatePassword(input) {
    const password = input.value;
    
    if (password && password.length < 6) {
        showFieldError(input, 'Пароль должен содержать минимум 6 символов');
        return false;
    } else {
        clearFieldError(input);
        return true;
    }
}

// Показать ошибку поля
function showFieldError(input, message) {
    clearFieldError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '5px';
    
    input.style.borderColor = '#dc3545';
    input.parentNode.appendChild(errorDiv);
}

// Очистить ошибку поля
function clearFieldError(input) {
    const existingError = input.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    input.style.borderColor = '';
}

// Показать общую ошибку
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'flash-message flash-error';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        ${message}
        <button class="flash-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    flashContainer.appendChild(errorDiv);
    
    // Автоматическое скрытие
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Создать контейнер для флеш сообщений
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Предварительный просмотр изображений
function initImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(input, e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// Показать предварительный просмотр изображения
function showImagePreview(input, imageSrc) {
    let preview = input.parentNode.querySelector('.image-preview');
    
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'image-preview';
        input.parentNode.appendChild(preview);
    }
    
    preview.innerHTML = `
        <div class="preview-container">
            <img src="${imageSrc}" alt="Предварительный просмотр">
            <button type="button" class="remove-preview" onclick="removeImagePreview(this)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Добавляем стили для предварительного просмотра
    if (!document.querySelector('#image-preview-styles')) {
        const styles = document.createElement('style');
        styles.id = 'image-preview-styles';
        styles.textContent = `
            .image-preview {
                margin-top: 10px;
            }
            .preview-container {
                position: relative;
                display: inline-block;
            }
            .preview-container img {
                width: 200px;
                height: 200px;
                object-fit: cover;
                border-radius: 10px;
                border: 2px solid #e9ecef;
            }
            .remove-preview {
                position: absolute;
                top: -10px;
                right: -10px;
                width: 30px;
                height: 30px;
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
            }
            .remove-preview:hover {
                background: #c82333;
            }
        `;
        document.head.appendChild(styles);
    }
}

// Удалить предварительный просмотр изображения
function removeImagePreview(button) {
    const preview = button.closest('.image-preview');
    const input = preview.parentNode.querySelector('input[type="file"]');
    
    if (input) {
        input.value = '';
    }
    
    preview.remove();
}

// Глобальная функция для удаления изображения (для совместимости)
function removeImage() {
    const imageInput = document.getElementById('image');
    const preview = imageInput.parentNode.querySelector('.image-preview');
    
    if (imageInput) {
        imageInput.value = '';
    }
    
    if (preview) {
        preview.remove();
    }
}

// Инициализация компонентов
function initComponents() {
    // Инициализация звездного рейтинга
    initStarRating();
    
    // Инициализация модальных окон
    initModals();
    
    // Инициализация табов
    initTabs();
    
    // Инициализация аккордеонов
    initAccordions();
}

// Звездный рейтинг
function initStarRating() {
    const starContainers = document.querySelectorAll('.stars');
    
    starContainers.forEach(container => {
        if (container.classList.contains('static-stars')) {
            return; // пропускаем интерактив на статичных звездах
        }
        const stars = container.querySelectorAll('i');
        
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', () => {
                highlightStars(stars, index + 1);
            });
            
            star.addEventListener('click', () => {
                setRating(stars, index + 1);
            });
        });
        
        container.addEventListener('mouseleave', () => {
            resetStars(stars);
        });
    });
}

// Подсветка звезд
function highlightStars(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.color = '#ffc107';
        } else {
            star.style.color = '#e9ecef';
        }
    });
}

// Установка рейтинга
function setRating(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
            star.style.color = '#ffc107';
        } else {
            star.classList.remove('active');
            star.style.color = '#e9ecef';
        }
    });
}

// Сброс звезд
function resetStars(stars) {
    stars.forEach(star => {
        if (!star.classList.contains('active')) {
            star.style.color = '#e9ecef';
        }
    });
}

// Модальные окна
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modals = document.querySelectorAll('.modal');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                showModal(modal);
            }
        });
    });
    
    // Закрытие модальных окон
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal') || e.target.classList.contains('modal-close')) {
            const modal = e.target.closest('.modal');
            if (modal) {
                hideModal(modal);
            }
        }
    });
    
    // Закрытие по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                hideModal(openModal);
            }
        }
    });
}

// Показать модальное окно
function showModal(modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// Скрыть модальное окно
function hideModal(modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
}

// Табы
function initTabs() {
    const tabContainers = document.querySelectorAll('.tabs');
    
    tabContainers.forEach(container => {
        const tabButtons = container.querySelectorAll('.tab-button');
        const tabContents = container.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Убираем активные классы
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Добавляем активные классы
                button.classList.add('active');
                const targetContent = container.querySelector(`[data-content="${targetTab}"]`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    });
}

// Аккордеоны
function initAccordions() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const accordion = header.closest('.accordion');
            const content = accordion.querySelector('.accordion-content');
            
            // Закрываем все остальные аккордеоны
            document.querySelectorAll('.accordion').forEach(acc => {
                if (acc !== accordion) {
                    acc.classList.remove('active');
                }
            });
            
            // Переключаем текущий аккордеон
            accordion.classList.toggle('active');
        });
    });
}

// Утилиты
const Utils = {
    // Дебаунс функция
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Троттлинг функция
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Форматирование даты
    formatDate: function(date) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return new Date(date).toLocaleDateString('ru-RU', options);
    },
    
    // Копирование в буфер обмена
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback для старых браузеров
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                return Promise.resolve();
            } catch (err) {
                return Promise.reject(err);
            } finally {
                document.body.removeChild(textArea);
            }
        }
    }
};

// Экспорт для использования в других скриптах
window.SweetieApp = {
    Utils,
    showError,
    showModal,
    hideModal
};


