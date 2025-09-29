#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления поля created_at из таблицы users
"""

from app import app, db
from sqlalchemy import text

def remove_users_created_at():
    """Удаляет поле created_at из таблицы users"""
    with app.app_context():
        try:
            # Проверяем, какие столбцы существуют в таблице users
            result = db.session.execute(text("DESCRIBE users"))
            columns = [row[0] for row in result.fetchall()]
            print(f"Текущие столбцы в users: {columns}")
            
            # Удаляем поле created_at если оно существует
            if 'created_at' in columns:
                try:
                    db.session.execute(text("ALTER TABLE users DROP COLUMN created_at"))
                    print("Удален столбец created_at из таблицы users")
                except Exception as e:
                    print(f"Ошибка при удалении столбца created_at: {e}")
            else:
                print("Столбец created_at не найден в таблице users")
            
            # Сохраняем изменения
            db.session.commit()
            print("Миграция завершена успешно!")
            
            # Показываем финальную структуру таблицы
            result = db.session.execute(text("DESCRIBE users"))
            final_columns = [row[0] for row in result.fetchall()]
            print(f"Финальные столбцы в users: {final_columns}")
            
        except Exception as e:
            print(f"Ошибка при выполнении миграции: {e}")
            db.session.rollback()

if __name__ == '__main__':
    remove_users_created_at()
