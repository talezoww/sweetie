#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/sweetie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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

def add_recipes():
    with app.app_context():
        try:
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                print("User not found")
                return False
            
            categories = {cat.name: cat for cat in Category.query.all()}
            ingredients = {ing.name: ing for ing in Ingredient.query.all()}
            
            recipes_data = [
                {
                    'title': 'Chocolate Muffins',
                    'description': 'Delicious chocolate muffins with chocolate chips',
                    'instructions': '1. Preheat oven to 200C\n2. Mix dry ingredients\n3. Mix wet ingredients\n4. Combine and bake for 20 minutes',
                    'prep_time': 15,
                    'cook_time': 20,
                    'servings': 12,
                    'category': 'Печенье',
                    'ingredients': [
                        {'ingredient': 'Мука', 'quantity': 200},
                        {'ingredient': 'Сахар', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 2},
                        {'ingredient': 'Масло сливочное', 'quantity': 80}
                    ]
                },
                {
                    'title': 'Tiramisu Classic',
                    'description': 'Traditional Italian dessert with coffee and mascarpone',
                    'instructions': '1. Make strong coffee\n2. Beat mascarpone with sugar\n3. Layer with ladyfingers\n4. Chill for 4 hours',
                    'prep_time': 45,
                    'cook_time': 0,
                    'servings': 6,
                    'category': 'Десерты',
                    'ingredients': [
                        {'ingredient': 'Сахар', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 4}
                    ]
                },
                {
                    'title': 'Red Velvet Cake',
                    'description': 'Bright and moist cake with cream cheese frosting',
                    'instructions': '1. Preheat oven to 180C\n2. Mix dry ingredients\n3. Beat butter with sugar\n4. Add eggs and vanilla\n5. Bake for 30 minutes',
                    'prep_time': 40,
                    'cook_time': 30,
                    'servings': 10,
                    'category': 'Торты',
                    'ingredients': [
                        {'ingredient': 'Мука', 'quantity': 250},
                        {'ingredient': 'Сахар', 'quantity': 200},
                        {'ingredient': 'Масло сливочное', 'quantity': 150},
                        {'ingredient': 'Яйца', 'quantity': 3}
                    ]
                },
                {
                    'title': 'Oatmeal Raisin Cookies',
                    'description': 'Healthy and tasty cookies with oats and raisins',
                    'instructions': '1. Preheat oven to 180C\n2. Mix oats, flour, salt\n3. Beat butter with sugar\n4. Combine and add raisins\n5. Bake for 15 minutes',
                    'prep_time': 20,
                    'cook_time': 15,
                    'servings': 24,
                    'category': 'Печенье',
                    'ingredients': [
                        {'ingredient': 'Мука', 'quantity': 100},
                        {'ingredient': 'Сахар', 'quantity': 80},
                        {'ingredient': 'Масло сливочное', 'quantity': 100},
                        {'ingredient': 'Яйца', 'quantity': 1}
                    ]
                },
                {
                    'title': 'Chocolate Truffles',
                    'description': 'Elegant chocolate truffles with various fillings',
                    'instructions': '1. Heat cream to boiling\n2. Pour over chopped chocolate\n3. Stir until smooth\n4. Add butter and liqueur\n5. Chill for 2 hours\n6. Form balls and roll in cocoa',
                    'prep_time': 30,
                    'cook_time': 0,
                    'servings': 20,
                    'category': 'Конфеты',
                    'ingredients': [
                        {'ingredient': 'Сахар', 'quantity': 50},
                        {'ingredient': 'Масло сливочное', 'quantity': 30}
                    ]
                }
            ]
            
            for recipe_data in recipes_data:
                existing = Recipe.query.filter_by(title=recipe_data['title']).first()
                if existing:
                    continue
                
                recipe = Recipe(
                    title=recipe_data['title'],
                    description=recipe_data['description'],
                    instructions=recipe_data['instructions'],
                    prep_time=recipe_data['prep_time'],
                    cook_time=recipe_data['cook_time'],
                    servings=recipe_data['servings'],
                    user_id=user.id,
                    category_id=categories[recipe_data['category']].id
                )
                db.session.add(recipe)
                db.session.flush()
                
                for ing_data in recipe_data['ingredients']:
                    if ing_data['ingredient'] in ingredients:
                        recipe_ingredient = RecipeIngredient(
                            quantity=ing_data['quantity'],
                            recipe_id=recipe.id,
                            ingredient_id=ingredients[ing_data['ingredient']].id
                        )
                        db.session.add(recipe_ingredient)
                
                print(f"Added recipe: {recipe_data['title']}")
            
            db.session.commit()
            print("Recipes added successfully!")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    add_recipes()
