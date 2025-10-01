#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления поля is_active из таблицы users
"""

from app import app, db
from sqlalchemy import text

def remove_is_active_field():
    """Удаляет поле is_active из таблицы users"""
    with app.app_context():
        try:
            # Проверяем, какие столбцы существуют в таблице users
            result = db.session.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"Текущие столбцы в users: {columns}")
            
            # Проверяем, существует ли поле is_active
            if 'is_active' in columns:
                try:
                    # Удаляем столбец is_active
                    db.session.execute(text("ALTER TABLE users DROP COLUMN is_active"))
                    print("Удален столбец: is_active")
                    
                    # Сохраняем изменения
                    db.session.commit()
                    print("Миграция завершена успешно!")
                    
                    # Показываем финальную структуру таблицы
                    result = db.session.execute(text("PRAGMA table_info(users)"))
                    final_columns = [row[1] for row in result.fetchall()]
                    print(f"Финальные столбцы в users: {final_columns}")
                    
                except Exception as e:
                    print(f"Ошибка при удалении столбца is_active: {e}")
                    db.session.rollback()
            else:
                print("Столбец is_active не найден в таблице users")
                
        except Exception as e:
            print(f"Ошибка при выполнении миграции: {e}")
            db.session.rollback()

if __name__ == '__main__':
    remove_is_active_field()
