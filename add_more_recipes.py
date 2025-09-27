#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления дополнительных рецептов
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

def add_more_recipes():
    """Добавление дополнительных рецептов"""
    with app.app_context():
        try:
            # Получаем тестового пользователя
            test_user = User.query.filter_by(email='test@example.com').first()
            if not test_user:
                print("Тестовый пользователь не найден!")
                return False
            
            # Получаем категории
            categories = {cat.name: cat for cat in Category.query.all()}
            
            # Получаем ингредиенты
            ingredients = {ing.name: ing for ing in Ingredient.query.all()}
            
            # Дополнительные рецепты
            additional_recipes = [
                {
                    'title': 'Шоколадные маффины',
                    'description': 'Нежные шоколадные маффины с кусочками шоколада - идеальный завтрак или перекус',
                    'instructions': '''1. Разогрейте духовку до 200°C
2. Смешайте муку, какао, сахар и разрыхлитель
3. В отдельной миске взбейте яйца с молоком и маслом
4. Соедините сухие и жидкие ингредиенты
5. Добавьте шоколадную крошку
6. Разложите по формочкам для маффинов
7. Выпекайте 15-20 минут до готовности''',
                    'prep_time': 15,
                    'cook_time': 20,
                    'servings': 12,
                    'category': 'Печенье',
                    'ingredients': [
                        {'ingredient': 'Мука', 'quantity': 200},
                        {'ingredient': 'Какао-порошок', 'quantity': 30},
                        {'ingredient': 'Сахар', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 2},
                        {'ingredient': 'Молоко', 'quantity': 150, 'unit': 'мл'},
                        {'ingredient': 'Масло сливочное', 'quantity': 80},
                        {'ingredient': 'Разрыхлитель', 'quantity': 10}
                    ]
                },
                {
                    'title': 'Тирамису классический',
                    'description': 'Знаменитый итальянский десерт с кофе, маскарпоне и савоярди',
                    'instructions': '''1. Приготовьте крепкий кофе и остудите
2. Взбейте маскарпоне с сахаром до однородности
3. Отдельно взбейте яичные желтки с сахаром
4. Соедините маскарпоне с желтками
5. Смочите савоярди в кофе
6. Выложите слоями: савоярди, крем, савоярди, крем
7. Посыпьте какао и охладите 4 часа''',
                    'prep_time': 45,
                    'cook_time': 0,
                    'servings': 6,
                    'category': 'Десерты',
                    'ingredients': [
                        {'ingredient': 'Маскарпоне', 'quantity': 500, 'unit': 'г'},
                        {'ingredient': 'Сахар', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 4},
                        {'ingredient': 'Кофе', 'quantity': 200, 'unit': 'мл'},
                        {'ingredient': 'Какао-порошок', 'quantity': 20},
                        {'ingredient': 'Савоярди', 'quantity': 200, 'unit': 'г'}
                    ]
                },
                {
                    'title': 'Красный бархат',
                    'description': 'Яркий и влажный торт с крем-чизом - настоящий праздник для глаз и вкуса',
                    'instructions': '''1. Разогрейте духовку до 180°C
2. Смешайте муку, какао, соль и разрыхлитель
3. Взбейте масло с сахаром до пышности
4. Добавьте яйца по одному
5. Добавьте ваниль и красный краситель
6. Поочередно добавляйте муку и пахту
7. Выпекайте 25-30 минут
8. Остудите и украсьте крем-чизом''',
                    'prep_time': 40,
                    'cook_time': 30,
                    'servings': 10,
                    'category': 'Торты',
                    'ingredients': [
                        {'ingredient': 'Мука', 'quantity': 250},
                        {'ingredient': 'Сахар', 'quantity': 200},
                        {'ingredient': 'Масло сливочное', 'quantity': 150},
                        {'ingredient': 'Яйца', 'quantity': 3},
                        {'ingredient': 'Пахта', 'quantity': 250, 'unit': 'мл'},
                        {'ingredient': 'Какао-порошок', 'quantity': 20},
                        {'ingredient': 'Ванилин', 'quantity': 5},
                        {'ingredient': 'Красный краситель', 'quantity': 10, 'unit': 'мл'}
                    ]
                },
                {
                    'title': 'Печенье с овсянкой и изюмом',
                    'description': 'Полезное и вкусное печенье с овсяными хлопьями и изюмом',
                    'instructions': '''1. Разогрейте духовку до 180°C
2. Смешайте овсяные хлопья, муку, соль и соду
3. Взбейте масло с сахаром до кремообразного состояния
4. Добавьте яйцо и ваниль
5. Соедините с сухими ингредиентами
6. Добавьте изюм
7. Сформируйте шарики и выложите на противень
8. Выпекайте 12-15 минут до золотистого цвета''',
                    'prep_time': 20,
                    'cook_time': 15,
                    'servings': 24,
                    'category': 'Печенье',
                    'ingredients': [
                        {'ingredient': 'Овсяные хлопья', 'quantity': 150, 'unit': 'г'},
                        {'ingredient': 'Мука', 'quantity': 100},
                        {'ingredient': 'Сахар', 'quantity': 80},
                        {'ingredient': 'Масло сливочное', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 1},
                        {'ingredient': 'Изюм', 'quantity': 50, 'unit': 'г'},
                        {'ingredient': 'Ванилин', 'quantity': 3}
                    ]
                },
                {
                    'title': 'Трюфели шоколадные',
                    'description': 'Изысканные шоколадные трюфели с различными начинками',
                    'instructions': '''1. Нагрейте сливки до кипения
2. Залейте горячими сливками мелко нарезанный шоколад
3. Размешайте до однородности
4. Добавьте сливочное масло и ликер
5. Охладите массу в холодильнике 2 часа
6. Сформируйте шарики
7. Обваляйте в какао или кокосовой стружке
8. Охладите перед подачей''',
                    'prep_time': 30,
                    'cook_time': 0,
                    'servings': 20,
                    'category': 'Конфеты',
                    'ingredients': [
                        {'ingredient': 'Темный шоколад', 'quantity': 200, 'unit': 'г'},
                        {'ingredient': 'Сливки', 'quantity': 100, 'unit': 'мл'},
                        {'ingredient': 'Масло сливочное', 'quantity': 30},
                        {'ingredient': 'Какао-порошок', 'quantity': 50},
                        {'ingredient': 'Ликер', 'quantity': 20, 'unit': 'мл'}
                    ]
                }
            ]
            
            print("Добавление дополнительных рецептов...")
            
            for recipe_data in additional_recipes:
                # Проверяем, не существует ли уже такой рецепт
                existing_recipe = Recipe.query.filter_by(title=recipe_data['title']).first()
                if existing_recipe:
                    print(f"Рецепт '{recipe_data['title']}' уже существует, пропускаем...")
                    continue
                
                # Создаем рецепт
                recipe = Recipe(
                    title=recipe_data['title'],
                    description=recipe_data['description'],
                    instructions=recipe_data['instructions'],
                    prep_time=recipe_data['prep_time'],
                    cook_time=recipe_data['cook_time'],
                    servings=recipe_data['servings'],
                    user_id=test_user.id,
                    category_id=categories[recipe_data['category']].id
                )
                db.session.add(recipe)
                db.session.flush()
                
                # Добавляем ингредиенты
                for ing_data in recipe_data['ingredients']:
                    ingredient = ingredients[ing_data['ingredient']]
                    recipe_ingredient = RecipeIngredient(
                        quantity=ing_data['quantity'],
                        notes=ing_data.get('notes', ''),
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id
                    )
                    db.session.add(recipe_ingredient)
                
                print(f"Добавлен рецепт: {recipe_data['title']}")
            
            # Сохраняем все изменения
            db.session.commit()
            print("Дополнительные рецепты успешно добавлены!")
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении рецептов: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("Добавление дополнительных рецептов...")
    success = add_more_recipes()
    
    if success:
        print("Готово! Теперь в базе данных больше рецептов.")
    else:
        print("Ошибка добавления рецептов.")
