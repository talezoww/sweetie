#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания профилей пользователей для существующих пользователей
"""

from app import app, db
from models import User, UserProfile

def migrate_user_profiles():
    """Создает профили для пользователей, у которых их нет"""
    with app.app_context():
        # Находим всех пользователей без профилей
        users_without_profiles = db.session.query(User).outerjoin(UserProfile).filter(UserProfile.id.is_(None)).all()
        
        print(f"Найдено {len(users_without_profiles)} пользователей без профилей")
        
        for user in users_without_profiles:
            # Создаем профиль для пользователя
            user_profile = UserProfile(
                user_id=user.id,
                first_name=user.username,
                bio=f"Профиль пользователя {user.username}"
            )
            db.session.add(user_profile)
            print(f"Создан профиль для пользователя: {user.username}")
        
        # Сохраняем изменения
        db.session.commit()
        print("Миграция завершена успешно!")

if __name__ == '__main__':
    migrate_user_profiles()
