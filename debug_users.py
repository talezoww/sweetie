#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для диагностики проблем с пользователями в базе данных
"""

from app import app, db
from models import User, Recipe, Category, Ingredient, RecipeIngredient, Comment, Rating, Favorite, UserProfile

def debug_users():
    """Диагностика пользователей в базе данных"""
    
    with app.app_context():
        print("=== Диагностика пользователей ===")
        print()
        
        # Проверяем подключение к базе данных
        try:
            db.session.execute("SELECT 1")
            print("✅ Подключение к базе данных работает")
        except Exception as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            return
        
        # Проверяем таблицы
        print("\n=== Проверка таблиц ===")
        try:
            users_count = User.query.count()
            print(f"👥 Пользователей в базе: {users_count}")
            
            if users_count > 0:
                print("\nСписок пользователей:")
                users = User.query.all()
                for user in users:
                    print(f"  ID: {user.id}, Username: {user.username}, Email: {user.email}")
            else:
                print("⚠️  В базе данных нет пользователей!")
                print("Запустите: python init_data.py")
                
        except Exception as e:
            print(f"❌ Ошибка при проверке пользователей: {e}")
        
        # Проверяем рецепты
        print("\n=== Проверка рецептов ===")
        try:
            recipes_count = Recipe.query.count()
            print(f"🍰 Рецептов в базе: {recipes_count}")
            
            if recipes_count > 0:
                print("\nСписок рецептов:")
                recipes = Recipe.query.all()
                for recipe in recipes:
                    user = User.query.get(recipe.user_id)
                    user_info = f"{user.username} (ID: {user.id})" if user else f"ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН (ID: {recipe.user_id})"
                    print(f"  ID: {recipe.id}, Название: {recipe.title}, Автор: {user_info}")
                    
                    # Проверяем, есть ли проблемы с внешними ключами
                    if not user:
                        print(f"    ⚠️  ПРОБЛЕМА: Пользователь с ID {recipe.user_id} не найден!")
                        
        except Exception as e:
            print(f"❌ Ошибка при проверке рецептов: {e}")
        
        # Проверяем категории
        print("\n=== Проверка категорий ===")
        try:
            categories_count = Category.query.count()
            print(f"📂 Категорий в базе: {categories_count}")
            
            if categories_count > 0:
                print("\nСписок категорий:")
                categories = Category.query.all()
                for category in categories:
                    print(f"  ID: {category.id}, Название: {category.name}")
            else:
                print("⚠️  В базе данных нет категорий!")
                print("Запустите: python init_data.py")
                
        except Exception as e:
            print(f"❌ Ошибка при проверке категорий: {e}")
        
        # Проверяем ингредиенты
        print("\n=== Проверка ингредиентов ===")
        try:
            ingredients_count = Ingredient.query.count()
            print(f"🥄 Ингредиентов в базе: {ingredients_count}")
            
            if ingredients_count > 0:
                print("\nСписок ингредиентов:")
                ingredients = Ingredient.query.all()
                for ingredient in ingredients:
                    print(f"  ID: {ingredient.id}, Название: {ingredient.name}, Единица: {ingredient.unit}")
            else:
                print("⚠️  В базе данных нет ингредиентов!")
                print("Запустите: python init_data.py")
                
        except Exception as e:
            print(f"❌ Ошибка при проверке ингредиентов: {e}")
        
        # Проверяем связи рецептов и ингредиентов
        print("\n=== Проверка связей рецепт-ингредиент ===")
        try:
            recipe_ingredients_count = RecipeIngredient.query.count()
            print(f"🔗 Связей рецепт-ингредиент: {recipe_ingredients_count}")
            
            if recipe_ingredients_count > 0:
                print("\nСписок связей:")
                recipe_ingredients = RecipeIngredient.query.all()
                for ri in recipe_ingredients:
                    recipe = Recipe.query.get(ri.recipe_id)
                    ingredient = Ingredient.query.get(ri.ingredient_id)
                    recipe_info = f"{recipe.title}" if recipe else f"РЕЦЕПТ НЕ НАЙДЕН (ID: {ri.recipe_id})"
                    ingredient_info = f"{ingredient.name}" if ingredient else f"ИНГРЕДИЕНТ НЕ НАЙДЕН (ID: {ri.ingredient_id})"
                    print(f"  Рецепт: {recipe_info}, Ингредиент: {ingredient_info}, Количество: {ri.quantity}")
                    
                    # Проверяем, есть ли проблемы с внешними ключами
                    if not recipe:
                        print(f"    ⚠️  ПРОБЛЕМА: Рецепт с ID {ri.recipe_id} не найден!")
                    if not ingredient:
                        print(f"    ⚠️  ПРОБЛЕМА: Ингредиент с ID {ri.ingredient_id} не найден!")
                        
        except Exception as e:
            print(f"❌ Ошибка при проверке связей: {e}")
        
        print("\n=== Рекомендации ===")
        if users_count == 0:
            print("1. Запустите: python init_data.py")
        if categories_count == 0:
            print("2. Запустите: python init_data.py")
        if ingredients_count == 0:
            print("3. Запустите: python init_data.py")
        
        print("4. Проверьте подключение к MySQL в config.py")
        print("5. Убедитесь, что база данных sweetie_db существует")
        print("6. Проверьте, что таблицы созданы (выполните create_database.sql в MySQL Workbench)")

def fix_orphaned_recipes():
    """Удаление рецептов без пользователей"""
    
    with app.app_context():
        print("\n=== Исправление проблемных данных ===")
        
        # Находим рецепты с несуществующими пользователями
        recipes = Recipe.query.all()
        orphaned_recipes = []
        
        for recipe in recipes:
            user = User.query.get(recipe.user_id)
            if not user:
                orphaned_recipes.append(recipe)
        
        if orphaned_recipes:
            print(f"Найдено {len(orphaned_recipes)} рецептов с несуществующими пользователями:")
            for recipe in orphaned_recipes:
                print(f"  - ID: {recipe.id}, Название: {recipe.title}, User ID: {recipe.user_id}")
            
            response = input("\nУдалить эти рецепты? (y/N): ")
            if response.lower() == 'y':
                for recipe in orphaned_recipes:
                    # Удаляем связанные данные
                    RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()
                    Comment.query.filter_by(recipe_id=recipe.id).delete()
                    Rating.query.filter_by(recipe_id=recipe.id).delete()
                    Favorite.query.filter_by(recipe_id=recipe.id).delete()
                    
                    # Удаляем рецепт
                    db.session.delete(recipe)
                
                db.session.commit()
                print("✅ Проблемные рецепты удалены")
            else:
                print("❌ Удаление отменено")
        else:
            print("✅ Проблемных рецептов не найдено")

if __name__ == '__main__':
    debug_users()
    
    response = input("\nПроверить и исправить проблемные данные? (y/N): ")
    if response.lower() == 'y':
        fix_orphaned_recipes()
