#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации базы данных с тестовыми данными
"""

from app import app, db, bcrypt
from models import User, Recipe, Category, Ingredient, RecipeIngredient, Comment, Rating, Favorite, UserProfile
from datetime import datetime

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if User.query.count() > 0:
            print("База данных уже содержит данные. Пропускаем инициализацию.")
            return
        
        print("Инициализация базы данных...")
        
        # Создаем тестового пользователя
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        test_user = User(
            username='testuser',
            email='test@example.com',
            password=hashed_password
        )
        db.session.add(test_user)
        db.session.flush()  # Получаем ID пользователя
        
        # Создаем профиль пользователя
        user_profile = UserProfile(
            first_name='Тестовый',
            last_name='Пользователь',
            bio='Люблю готовить сладости и делиться рецептами',
            user_id=test_user.id
        )
        db.session.add(user_profile)
        
        # Создаем категории если их нет
        categories_data = [
            {'name': 'Торты', 'description': 'Праздничные и повседневные торты'},
            {'name': 'Печенье', 'description': 'Хрустящее печенье и мягкие кексы'},
            {'name': 'Десерты', 'description': 'Холодные и горячие десерты'},
            {'name': 'Конфеты', 'description': 'Домашние конфеты и сладости'}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
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
            ingredient = Ingredient.query.filter_by(name=ing_data['name']).first()
            if not ingredient:
                ingredient = Ingredient(**ing_data)
                db.session.add(ingredient)
                db.session.flush()
            ingredients[ing_data['name']] = ingredient
        
        # Создаем тестовые рецепты
        recipes_data = [
            {
                'title': 'Классический шоколадный торт',
                'description': 'Нежный шоколадный торт с кремом - идеальный десерт для особых случаев',
                'instructions': '''1. Разогрейте духовку до 180°C
2. Смешайте муку, какао и разрыхлитель
3. Взбейте масло с сахаром до пышности
4. Добавьте яйца по одному
5. Добавьте сухие ингредиенты
6. Выпекайте 25-30 минут
7. Остудите и украсьте кремом''',
                'prep_time': 30,
                'cook_time': 30,
                'servings': 8,
                'category': 'Торты',
                'ingredients': [
                    {'name': 'Мука', 'quantity': 200, 'notes': 'просеянная'},
                    {'name': 'Сахар', 'quantity': 150},
                    {'name': 'Какао-порошок', 'quantity': 50},
                    {'name': 'Яйца', 'quantity': 3},
                    {'name': 'Масло сливочное', 'quantity': 100},
                    {'name': 'Разрыхлитель', 'quantity': 10}
                ]
            },
            {
                'title': 'Печенье с шоколадной крошкой',
                'description': 'Хрустящее печенье с кусочками шоколада - любимое лакомство детей и взрослых',
                'instructions': '''1. Разогрейте духовку до 190°C
2. Смешайте масло с сахаром
3. Добавьте яйцо и ванилин
4. Добавьте муку и соль
5. Добавьте шоколадную крошку
6. Сформируйте шарики
7. Выпекайте 10-12 минут''',
                'prep_time': 15,
                'cook_time': 12,
                'servings': 24,
                'category': 'Печенье',
                'ingredients': [
                    {'name': 'Мука', 'quantity': 250},
                    {'name': 'Сахар', 'quantity': 100},
                    {'name': 'Масло сливочное', 'quantity': 125},
                    {'name': 'Яйца', 'quantity': 1},
                    {'name': 'Ванилин', 'quantity': 5}
                ]
            },
            {
                'title': 'Тирамису',
                'description': 'Классический итальянский десерт с кофе и маскарпоне',
                'instructions': '''1. Приготовьте кофе и остудите
2. Взбейте маскарпоне с сахаром
3. Добавьте яичные желтки
4. Смочите савоярди в кофе
5. Выложите слоями
6. Охладите 4 часа
7. Посыпьте какао перед подачей''',
                'prep_time': 45,
                'cook_time': 0,
                'servings': 6,
                'category': 'Десерты',
                'ingredients': [
                    {'name': 'Маскарпоне', 'quantity': 500, 'unit': 'г'},
                    {'name': 'Сахар', 'quantity': 100},
                    {'name': 'Яйца', 'quantity': 4},
                    {'name': 'Кофе', 'quantity': 200, 'unit': 'мл'},
                    {'name': 'Какао-порошок', 'quantity': 20}
                ]
            }
        ]
        
        for recipe_data in recipes_data:
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
                ingredient = ingredients[ing_data['name']]
                recipe_ingredient = RecipeIngredient(
                    quantity=ing_data['quantity'],
                    notes=ing_data.get('notes', ''),
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id
                )
                db.session.add(recipe_ingredient)
            
            # Добавляем комментарии
            comments_data = [
                'Отличный рецепт! Получилось очень вкусно.',
                'Спасибо за подробные инструкции!',
                'Мой любимый рецепт, готовлю уже не первый раз.'
            ]
            
            for comment_text in comments_data:
                comment = Comment(
                    content=comment_text,
                    user_id=test_user.id,
                    recipe_id=recipe.id
                )
                db.session.add(comment)
            
            # Добавляем оценки
            rating = Rating(
                rating=5,
                user_id=test_user.id,
                recipe_id=recipe.id
            )
            db.session.add(rating)
        
        # Сохраняем все изменения
        db.session.commit()
        print("База данных успешно инициализирована!")
        print("Создан тестовый пользователь:")
        print("Email: test@example.com")
        print("Пароль: password123")

if __name__ == '__main__':
    init_database()


