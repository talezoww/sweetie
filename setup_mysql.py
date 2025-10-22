#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматической настройки MySQL базы данных для Sweetie
"""

import os
import sys
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

def setup_mysql_database():
    """Настройка MySQL базы данных"""
    
    print("=== Настройка MySQL для Sweetie ===")
    print()
    print("⚠️  ВАЖНО: Проект работает ТОЛЬКО с MySQL!")
    print("💡 РЕКОМЕНДАЦИЯ: Используйте MySQL Workbench для удобной работы с базой данных!")
    print("📖 Подробная инструкция: MYSQL_WORKBENCH_GUIDE.md")
    print("🚫 SQLite НЕ ПОДДЕРЖИВАЕТСЯ!")
    print()
    
    # Получаем данные подключения от пользователя
    print("Введите данные для подключения к MySQL:")
    print("(Эти же данные используйте в MySQL Workbench)")
    host = input("Хост (по умолчанию localhost): ").strip() or "localhost"
    port = input("Порт (по умолчанию 3306): ").strip() or "3306"
    username = input("Имя пользователя (по умолчанию root): ").strip() or "root"
    password = input("Пароль MySQL: ").strip()
    database = input("Имя базы данных (по умолчанию sweetie_db): ").strip() or "sweetie_db"
    
    print(f"\nПодключение к MySQL: {username}@{host}:{port}")
    
    try:
        # Подключаемся к MySQL серверу
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        print("✓ Подключение к MySQL успешно!")
        
        # Создаем базу данных
        print(f"Создание базы данных '{database}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {database}")
        print(f"✓ База данных '{database}' создана/выбрана")
        
        # Читаем и выполняем SQL скрипт
        print("Создание таблиц...")
        with open('create_database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Разбиваем скрипт на команды
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for command in commands:
            if command and not command.startswith('CREATE DATABASE') and not command.startswith('USE '):
                try:
                    cursor.execute(command)
                    print(f"✓ {command[:50]}...")
                except Exception as e:
                    print(f"⚠ Ошибка в команде: {command[:50]}... - {e}")
        
        connection.commit()
        print("✓ Таблицы созданы успешно!")
        
        # Проверяем созданные таблицы
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nСоздано таблиц: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        
        # Обновляем конфигурацию
        update_config(host, port, username, password, database)
        
        print("\n=== Настройка завершена! ===")
        print("✅ База данных создана и настроена")
        print("📊 Для работы с базой данных используйте MySQL Workbench")
        print("🔗 Подключение: {}:{} (пользователь: {})".format(host, port, username))
        print("🗄️ База данных: {}".format(database))
        print()
        print("Следующие шаги:")
        print("1. Откройте MySQL Workbench")
        print("2. Создайте подключение с теми же данными")
        print("3. Запустите приложение: python run.py")
        print("4. Откройте http://localhost:5000")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при настройке базы данных: {e}")
        print("\nВозможные решения:")
        print("1. Убедитесь, что MySQL сервер запущен")
        print("2. Проверьте правильность данных подключения")
        print("3. Убедитесь, что пользователь имеет права на создание баз данных")
        return False

def update_config(host, port, username, password, database):
    """Обновление конфигурации"""
    
    # Создаем строку подключения
    db_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    
    # Читаем текущий config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Обновляем строку подключения
    old_uri = "mysql+pymysql://root:password@localhost/sweetie_db"
    new_content = content.replace(old_uri, db_uri)
    
    # Записываем обновленный файл
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Конфигурация обновлена: {db_uri}")

def create_test_data():
    """Создание тестовых данных"""
    
    print("\nСоздание тестовых данных...")
    
    # Создаем приложение Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/sweetie_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Инициализируем расширения
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    
    # Импортируем модели
    from models import User, Category, Recipe, Ingredient, RecipeIngredient, Comment, Rating
    
    with app.app_context():
        try:
            # Проверяем, есть ли уже данные
            if User.query.count() > 0:
                print("✓ База данных уже содержит данные")
                return True
            
            # Создаем тестового пользователя
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            test_user = User(
                username='testuser',
                email='test@example.com',
                password=hashed_password
            )
            db.session.add(test_user)
            db.session.flush()
            
            # Создаем тестовый рецепт
            recipe = Recipe(
                title='Классический шоколадный торт',
                description='Нежный шоколадный торт с кремом',
                instructions='''1. Разогрейте духовку до 180°C
2. Смешайте муку, какао и разрыхлитель
3. Взбейте масло с сахаром до пышности
4. Добавьте яйца по одному
5. Добавьте сухие ингредиенты
6. Выпекайте 25-30 минут''',
                prep_time=30,
                cook_time=30,
                servings=8,
                user_id=test_user.id
            )
            db.session.add(recipe)
            db.session.commit()
            
            print("✓ Тестовые данные созданы!")
            print("Тестовый пользователь:")
            print("  Email: test@example.com")
            print("  Пароль: password123")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при создании тестовых данных: {e}")
            return False

if __name__ == '__main__':
    print("Добро пожаловать в настройку Sweetie!")
    print("Этот скрипт поможет настроить MySQL базу данных для вашего проекта.")
    print()
    
    # Проверяем наличие SQL файла
    if not os.path.exists('create_database.sql'):
        print("❌ Файл create_database.sql не найден!")
        print("Убедитесь, что вы находитесь в корневой папке проекта.")
        sys.exit(1)
    
    # Настраиваем базу данных
    if setup_mysql_database():
        # Создаем тестовые данные
        create_test_data()
    else:
        print("Настройка не завершена. Проверьте ошибки выше.")
        sys.exit(1)
