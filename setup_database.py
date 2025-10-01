#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для настройки базы данных Sweetie
"""

import pymysql
import os
from config import config

def setup_database():
    """Создание и настройка базы данных"""
    
    # Получаем конфигурацию
    config_name = os.environ.get('FLASK_ENV', 'development')
    app_config = config[config_name]
    
    # Парсим строку подключения
    db_uri = app_config.SQLALCHEMY_DATABASE_URI
    # mysql+pymysql://username:password@localhost/database
    if db_uri.startswith('mysql+pymysql://'):
        db_uri = db_uri.replace('mysql+pymysql://', '')
    
    # Разбираем строку подключения
    if '@' in db_uri:
        auth_part, host_db = db_uri.split('@', 1)
        if ':' in auth_part:
            username, password = auth_part.split(':', 1)
        else:
            username = auth_part
            password = ''
        
        if '/' in host_db:
            host, database = host_db.split('/', 1)
        else:
            host = host_db
            database = ''
    else:
        username = 'root'
        password = ''
        host = 'localhost'
        database = 'sweetie_db'
    
    print(f"Подключение к MySQL: {username}@{host}")
    
    try:
        # Подключаемся к MySQL (без указания базы данных)
        connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Создаем базу данных если её нет
        print("Создание базы данных...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS sweetie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE sweetie_db")
        
        # Читаем и выполняем SQL скрипт
        print("Выполнение SQL скрипта...")
        with open('create_database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Разбиваем скрипт на отдельные команды
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for command in commands:
            if command:
                try:
                    cursor.execute(command)
                    print(f"Выполнено: {command[:50]}...")
                except Exception as e:
                    print(f"Ошибка в команде: {command[:50]}... - {e}")
        
        connection.commit()
        print("База данных успешно настроена!")
        
        # Проверяем созданные таблицы
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Создано таблиц: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"Ошибка при настройке базы данных: {e}")
        return False

if __name__ == '__main__':
    print("Настройка базы данных Sweetie...")
    success = setup_database()
    
    if success:
        print("\nБаза данных готова!")
        print("Теперь можно запустить приложение: python run.py")
    else:
        print("\nОшибка настройки базы данных")
        print("Проверьте настройки подключения в config.py")
