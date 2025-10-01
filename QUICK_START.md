# 🚀 Быстрый старт Sweetie

## Установка за 5 минут

### 1. Клонирование и настройка окружения
```bash
git clone <repository-url>
cd yana
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных
```sql
-- В MySQL создайте базу данных
CREATE DATABASE sweetie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Настройка подключения
Отредактируйте `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost/sweetie_db'
```

### 5. Запуск
```bash
python run.py
```

### 6. Открыть в браузере
```
http://localhost:5000
```

## Тестовые данные

Для создания тестовых данных выполните:
```bash
python init_data.py
```

Это создаст:
- Пользователя: `test@example.com` / `password123`
- Категории рецептов
- Несколько тестовых рецептов

## Основные команды

```bash
# Запуск приложения
python run.py

# Создание таблиц БД
python create_tables.py

# Инициализация данных
python init_data.py

# Добавление рецептов
python add_more_recipes.py
```

## Структура URL

- `/` - главная страница
- `/register` - регистрация
- `/login` - вход
- `/recipes` - каталог рецептов
- `/add_recipe` - добавить рецепт
- `/my_recipes` - мои рецепты
- `/favorites` - избранное

## Возможные проблемы

### Ошибка подключения к MySQL
- Проверьте, что MySQL запущен
- Убедитесь в правильности данных в `config.py`

### ModuleNotFoundError
- Активируйте виртуальное окружение
- Переустановите зависимости: `pip install -r requirements.txt`

### Ошибка загрузки файлов
- Создайте папку `static/uploads`
- Проверьте права доступа

## Готово! 🎉

Теперь вы можете:
- Регистрироваться и входить в систему
- Добавлять рецепты с изображениями
- Просматривать каталог рецептов
- Оставлять комментарии и оценки
- Добавлять рецепты в избранное
