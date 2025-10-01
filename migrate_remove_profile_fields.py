#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления ненужных полей из таблицы user_profiles
"""

from app import app, db
from sqlalchemy import text

def remove_profile_fields():
    """Удаляет ненужные поля из таблицы user_profiles"""
    with app.app_context():
        try:
            # Проверяем, какие столбцы существуют
            result = db.session.execute(text("DESCRIBE user_profiles"))
            columns = [row[0] for row in result.fetchall()]
            print(f"Текущие столбцы в user_profiles: {columns}")
            
            # Удаляем ненужные столбцы если они существуют
            fields_to_remove = ['last_name', 'avatar_path', 'phone', 'birth_date']
            
            for field in fields_to_remove:
                if field in columns:
                    try:
                        db.session.execute(text(f"ALTER TABLE user_profiles DROP COLUMN {field}"))
                        print(f"Удален столбец: {field}")
                    except Exception as e:
                        print(f"Ошибка при удалении столбца {field}: {e}")
                else:
                    print(f"Столбец {field} не найден, пропускаем")
            
            # Сохраняем изменения
            db.session.commit()
            print("Миграция завершена успешно!")
            
            # Показываем финальную структуру таблицы
            result = db.session.execute(text("DESCRIBE user_profiles"))
            final_columns = [row[0] for row in result.fetchall()]
            print(f"Финальные столбцы в user_profiles: {final_columns}")
            
        except Exception as e:
            print(f"Ошибка при выполнении миграции: {e}")
            db.session.rollback()

if __name__ == '__main__':
    remove_profile_fields()
