#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания таблиц и тестовых данных
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# Создаем приложение
app = Flask(__name__)

# Конфигурация
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/sweetie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем расширения
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модели (копируем из models.py)
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    unit = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(255))
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_rating'),)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_favorite'),)

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    avatar_path = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

def init_database():
    """Инициализация базы данных"""
    with app.app_context():
        try:
            # Создаем таблицы
            print("Создание таблиц...")
            db.create_all()
            
            # Проверяем, есть ли уже данные
            if User.query.count() > 0:
                print("База данных уже содержит данные.")
                return True
            
            print("Создание тестовых данных...")
            
            # Создаем тестового пользователя
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            test_user = User(
                username='testuser',
                email='test@example.com',
                password=hashed_password
            )
            db.session.add(test_user)
            db.session.flush()
            
            # Создаем категории
            categories_data = [
                {'name': 'Торты', 'description': 'Праздничные и повседневные торты'},
                {'name': 'Печенье', 'description': 'Хрустящее печенье и мягкие кексы'},
                {'name': 'Десерты', 'description': 'Холодные и горячие десерты'},
                {'name': 'Конфеты', 'description': 'Домашние конфеты и сладости'}
            ]
            
            categories = {}
            for cat_data in categories_data:
                category = Category(**cat_data)
                db.session.add(category)
                db.session.flush()
                categories[cat_data['name']] = category
            
            # Создаем ингредиенты
            ingredients_data = [
                {'name': 'Мука', 'unit': 'г'},
                {'name': 'Сахар', 'unit': 'г'},
                {'name': 'Яйца', 'unit': 'шт'},
                {'name': 'Масло сливочное', 'unit': 'г'},
                {'name': 'Молоко', 'unit': 'мл'},
                {'name': 'Соль', 'unit': 'г'},
                {'name': 'Разрыхлитель', 'unit': 'г'},
                {'name': 'Ванилин', 'unit': 'г'},
                {'name': 'Какао-порошок', 'unit': 'г'},
                {'name': 'Сметана', 'unit': 'г'}
            ]
            
            ingredients = {}
            for ing_data in ingredients_data:
                ingredient = Ingredient(**ing_data)
                db.session.add(ingredient)
                db.session.flush()
                ingredients[ing_data['name']] = ingredient
            
            # Создаем тестовый рецепт
            recipe = Recipe(
                title='Классический шоколадный торт',
                description='Нежный шоколадный торт с кремом - идеальный десерт для особых случаев',
                instructions='''1. Разогрейте духовку до 180°C
2. Смешайте муку, какао и разрыхлитель
3. Взбейте масло с сахаром до пышности
4. Добавьте яйца по одному
5. Добавьте сухие ингредиенты
6. Выпекайте 25-30 минут
7. Остудите и украсьте кремом''',
                prep_time=30,
                cook_time=30,
                servings=8,
                user_id=test_user.id,
                category_id=categories['Торты'].id
            )
            db.session.add(recipe)
            db.session.flush()
            
            # Добавляем ингредиенты к рецепту
            recipe_ingredients_data = [
                {'ingredient': 'Мука', 'quantity': 200, 'notes': 'просеянная'},
                {'ingredient': 'Сахар', 'quantity': 150},
                {'ingredient': 'Какао-порошок', 'quantity': 50},
                {'ingredient': 'Яйца', 'quantity': 3},
                {'ingredient': 'Масло сливочное', 'quantity': 100},
                {'ingredient': 'Разрыхлитель', 'quantity': 10}
            ]
            
            for ing_data in recipe_ingredients_data:
                recipe_ingredient = RecipeIngredient(
                    quantity=ing_data['quantity'],
                    notes=ing_data.get('notes', ''),
                    recipe_id=recipe.id,
                    ingredient_id=ingredients[ing_data['ingredient']].id
                )
                db.session.add(recipe_ingredient)
            
            # Добавляем комментарий
            comment = Comment(
                content='Отличный рецепт! Получилось очень вкусно.',
                user_id=test_user.id,
                recipe_id=recipe.id
            )
            db.session.add(comment)
            
            # Добавляем оценку
            rating = Rating(
                rating=5,
                user_id=test_user.id,
                recipe_id=recipe.id
            )
            db.session.add(rating)
            
            # Сохраняем все изменения
            db.session.commit()
            print("База данных успешно инициализирована!")
            print("Тестовый пользователь:")
            print("Email: test@example.com")
            print("Пароль: password123")
            return True
            
        except Exception as e:
            print(f"Ошибка при инициализации: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("Инициализация базы данных...")
    success = init_database()
    
    if success:
        print("Готово! Теперь можно запустить приложение.")
    else:
        print("Ошибка инициализации базы данных.")
