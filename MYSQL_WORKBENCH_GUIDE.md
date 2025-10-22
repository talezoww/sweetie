# 🗄️ Подробная инструкция по настройке MySQL Workbench для Sweetie

## 📋 Содержание
1. [Установка MySQL и MySQL Workbench](#установка)
2. [Настройка подключения](#настройка-подключения)
3. [Создание базы данных](#создание-базы-данных)
4. [Импорт структуры](#импорт-структуры)
5. [Проверка работы](#проверка-работы)
6. [Решение проблем](#решение-проблем)

## 🚀 Установка MySQL и MySQL Workbench

### Windows (рекомендуется):
1. Перейдите на [mysql.com/downloads/installer](https://dev.mysql.com/downloads/installer/)
2. Скачайте **MySQL Installer for Windows**
3. При установке выберите:
   - ✅ MySQL Server
   - ✅ MySQL Workbench
   - ✅ MySQL Shell (опционально)
4. Установите пароль для пользователя `root`

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install mysql-server mysql-workbench
sudo mysql_secure_installation
```

### macOS:
```bash
brew install mysql mysql-workbench
brew services start mysql
```

## 🔧 Настройка подключения

### Шаг 1: Запуск MySQL Workbench
1. Запустите **MySQL Workbench**
2. В главном окне нажмите **"+"** рядом с "MySQL Connections"

### Шаг 2: Создание подключения
Заполните форму:
- **Connection Name:** `Sweetie Local`
- **Hostname:** `localhost`
- **Port:** `3306`
- **Username:** `root`
- **Password:** `[ваш пароль MySQL]`
- **Default Schema:** оставьте пустым

### Шаг 3: Тест подключения
1. Нажмите **"Test Connection"**
2. Если все OK - нажмите **"OK"**
3. Если ошибка - проверьте пароль и запущен ли MySQL сервер

## 🗃️ Создание базы данных

### Шаг 1: Открытие подключения
1. Дважды кликните на созданное подключение
2. Дождитесь загрузки интерфейса

### Шаг 2: Создание базы данных
В SQL редакторе выполните:
```sql
CREATE DATABASE sweetie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Шаг 3: Выбор базы данных
```sql
USE sweetie_db;
```

## 📥 Импорт структуры

### Способ 1: Через SQL скрипт (рекомендуется)
1. **File** → **Open SQL Script**
2. Найдите файл `create_database.sql` в папке проекта
3. Выберите файл и нажмите **"Open"**
4. Нажмите **Ctrl+Shift+Enter** для выполнения скрипта
5. Дождитесь завершения выполнения

### Способ 2: Копирование SQL команд
1. Откройте файл `create_database.sql` в текстовом редакторе
2. Скопируйте весь содержимое
3. Вставьте в SQL редактор MySQL Workbench
4. Выполните (Ctrl+Shift+Enter)

## ✅ Проверка работы

### Шаг 1: Проверка таблиц
```sql
SHOW TABLES;
```
Должны появиться таблицы:
- users
- categories
- recipes
- ingredients
- recipe_ingredients
- comments
- ratings
- favorites
- user_profiles

### Шаг 2: Проверка данных
```sql
SELECT * FROM categories;
SELECT * FROM ingredients;
```

### Шаг 3: Проверка структуры таблицы
```sql
DESCRIBE users;
DESCRIBE recipes;
```

## 🔧 Настройка проекта

### Шаг 1: Редактирование config.py
Откройте файл `config.py` и измените строку подключения:
```python
# Замените YOUR_PASSWORD на ваш MySQL пароль
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/sweetie_db'
```

### Шаг 2: Добавление тестовых данных
```bash
python init_data.py
```

### Шаг 3: Запуск приложения
```bash
python run.py
```

### Шаг 4: Проверка в браузере
Откройте `http://localhost:5000`

## 🔍 Мониторинг в MySQL Workbench

### Просмотр пользователей:
```sql
USE sweetie_db;
SELECT id, username, email, created_at FROM users;
```

### Просмотр рецептов:
```sql
SELECT id, title, prep_time, cook_time, servings, created_at FROM recipes;
```

### Просмотр комментариев:
```sql
SELECT c.content, u.username, r.title 
FROM comments c 
JOIN users u ON c.user_id = u.id 
JOIN recipes r ON c.recipe_id = r.id;
```

### Просмотр рейтингов:
```sql
SELECT r.title, AVG(rt.rating) as avg_rating, COUNT(rt.rating) as rating_count
FROM recipes r 
LEFT JOIN ratings rt ON r.id = rt.recipe_id 
GROUP BY r.id, r.title;
```

## 🛠️ Решение проблем

### Проблема: "Access denied for user 'root'@'localhost'"
**Решение:**
1. В MySQL Workbench выполните:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

### Проблема: "Can't connect to MySQL server"
**Решение:**
1. **Windows:** Проверьте службы Windows - MySQL должен быть запущен
2. **Linux:** `sudo systemctl start mysql`
3. **macOS:** `brew services start mysql`

### Проблема: "Unknown database 'sweetie_db'"
**Решение:**
1. Убедитесь, что база данных создана:
```sql
SHOW DATABASES;
```
2. Если нет - создайте заново:
```sql
CREATE DATABASE sweetie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Проблема: "Table doesn't exist"
**Решение:**
1. Убедитесь, что вы в правильной базе данных:
```sql
USE sweetie_db;
SHOW TABLES;
```
2. Если таблиц нет - выполните скрипт `create_database.sql` заново

## 📊 Полезные SQL запросы для разработки

### Статистика проекта:
```sql
-- Количество пользователей
SELECT COUNT(*) as total_users FROM users;

-- Количество рецептов
SELECT COUNT(*) as total_recipes FROM recipes;

-- Количество комментариев
SELECT COUNT(*) as total_comments FROM comments;

-- Средний рейтинг рецептов
SELECT AVG(rating) as avg_rating FROM ratings;

-- Топ-5 рецептов по рейтингу
SELECT r.title, AVG(rt.rating) as avg_rating, COUNT(rt.rating) as votes
FROM recipes r 
LEFT JOIN ratings rt ON r.id = rt.recipe_id 
GROUP BY r.id, r.title 
ORDER BY avg_rating DESC 
LIMIT 5;
```

### Очистка тестовых данных:
```sql
-- ВНИМАНИЕ: Это удалит все данные!
DELETE FROM ratings;
DELETE FROM comments;
DELETE FROM favorites;
DELETE FROM recipe_ingredients;
DELETE FROM recipes;
DELETE FROM users;
DELETE FROM categories;
DELETE FROM ingredients;
```

## 🎯 Следующие шаги

После успешной настройки:
1. Запустите приложение: `python run.py`
2. Откройте `http://localhost:5000`
3. Зарегистрируйтесь или войдите с тестовыми данными
4. Создайте свой первый рецепт!
5. Проверьте данные в MySQL Workbench

---

**Удачной настройки! 🍰✨**
