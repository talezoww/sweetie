# Инструкция по установке Sweetie

## Системные требования

- Python 3.8 или выше
- MySQL 5.7 или выше
- pip (менеджер пакетов Python)

## Пошаговая установка

### 1. Клонирование проекта

```bash
git clone <repository-url>
cd sweetie
```

### 2. Создание виртуального окружения

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных MySQL

1. **Создайте базу данных:**
```sql
CREATE DATABASE sweetie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Создайте пользователя (опционально):**
```sql
CREATE USER 'sweetie_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON sweetie_db.* TO 'sweetie_user'@'localhost';
FLUSH PRIVILEGES;
```

3. **Импортируйте структуру базы данных:**
```bash
mysql -u root -p sweetie_db < create_database.sql
```

### 5. Настройка конфигурации

Отредактируйте файл `config.py` или установите переменные окружения:

```bash
# Для Windows
set DATABASE_URL=mysql+pymysql://username:password@localhost/sweetie_db
set SECRET_KEY=your-secret-key-here

# Для Linux/Mac
export DATABASE_URL=mysql+pymysql://username:password@localhost/sweetie_db
export SECRET_KEY=your-secret-key-here
```

### 6. Инициализация данных (опционально)

Для создания тестовых данных выполните:

```bash
python init_data.py
```

Это создаст:
- Тестового пользователя (email: test@example.com, пароль: password123)
- Базовые категории
- Несколько тестовых рецептов

### 7. Запуск приложения

```bash
python run.py
```

Или:

```bash
python app.py
```

### 8. Открытие в браузере

Перейдите по адресу: `http://localhost:5000`

## Альтернативный способ запуска

### Использование Flask CLI

```bash
# Установка переменных окружения
export FLASK_APP=app.py
export FLASK_ENV=development

# Запуск
flask run
```

## Настройка для продакшена

### 1. Установка WSGI сервера

```bash
pip install gunicorn
```

### 2. Создание WSGI файла

Создайте файл `wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### 3. Запуск с Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## Возможные проблемы и решения

### Ошибка подключения к MySQL

1. Убедитесь, что MySQL запущен
2. Проверьте правильность данных подключения в `config.py`
3. Убедитесь, что пользователь имеет права доступа к базе данных

### Ошибка "ModuleNotFoundError"

1. Убедитесь, что виртуальное окружение активировано
2. Переустановите зависимости: `pip install -r requirements.txt`

### Ошибка "Permission denied" при загрузке файлов

1. Убедитесь, что папка `static/uploads` существует
2. Проверьте права доступа к папке

### Проблемы с кодировкой

1. Убедитесь, что база данных создана с кодировкой `utf8mb4`
2. Проверьте настройки MySQL

## Структура проекта после установки

```
sweetie/
├── app.py                 # Основное приложение
├── models.py             # Модели базы данных
├── config.py            # Конфигурация
├── run.py               # Файл запуска
├── init_data.py         # Инициализация данных
├── create_database.sql  # SQL скрипт
├── requirements.txt     # Зависимости
├── README.md           # Документация
├── INSTALL.md          # Инструкция по установке
├── templates/          # HTML шаблоны
├── static/            # Статические файлы
│   ├── css/
│   ├── js/
│   └── uploads/
└── venv/              # Виртуальное окружение
```

## Проверка установки

После запуска приложения проверьте:

1. ✅ Главная страница загружается
2. ✅ Регистрация работает
3. ✅ Авторизация работает
4. ✅ Добавление рецептов работает
5. ✅ Просмотр рецептов работает
6. ✅ Загрузка изображений работает

## Поддержка

При возникновении проблем:

1. Проверьте логи приложения
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки базы данных
4. Обратитесь к документации Flask и SQLAlchemy


