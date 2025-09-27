from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import re
from datetime import datetime
from config import config

app = Flask(__name__)

# Загружаем конфигурацию
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Создаем папку для загрузок если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Инициализируем расширения
bcrypt = Bcrypt()

# Инициализируем расширения с приложением
bcrypt.init_app(app)

# Импортируем модели и db
from models import db, User, Recipe, Category, Ingredient, RecipeIngredient, Comment, Rating, Favorite, UserProfile

# Инициализируем db с приложением
db.init_app(app)

# Создаем таблицы
with app.app_context():
    db.create_all()

# Валидация email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Валидация пароля
def is_valid_password(password):
    return len(password) >= 6

# Декоратор для проверки авторизации
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Валидация
        if not is_valid_email(email):
            flash('Некорректный email адрес', 'error')
            return render_template('register.html')
        
        if not is_valid_password(password):
            flash('Пароль должен содержать минимум 6 символов', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html')
        
        # Проверка существования пользователя
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('register.html')
        
        # Создание пользователя
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Добро пожаловать!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/recipes')
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients, comments=comments)

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructions = request.form['instructions']
        prep_time = request.form['prep_time']
        cook_time = request.form['cook_time']
        servings = request.form['servings']
        
        # Обработка загрузки изображения
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Добавляем timestamp для уникальности имени файла
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename
        
        # Создание рецепта
        recipe = Recipe(
            title=title,
            description=description,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            image_path=image_path,
            user_id=session['user_id']
        )
        
        db.session.add(recipe)
        db.session.flush()  # Получаем ID рецепта
        
        # Обработка ингредиентов
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        ingredient_units = request.form.getlist('ingredient_unit[]')
        
        for i, name in enumerate(ingredient_names):
            if name.strip():  # Проверяем, что название не пустое
                # Ищем существующий ингредиент или создаем новый
                ingredient = Ingredient.query.filter_by(name=name.strip()).first()
                if not ingredient:
                    ingredient = Ingredient(name=name.strip(), unit=ingredient_units[i] if i < len(ingredient_units) else 'г')
                    db.session.add(ingredient)
                    db.session.flush()
                
                # Создаем связь рецепта с ингредиентом
                quantity = float(ingredient_quantities[i]) if i < len(ingredient_quantities) and ingredient_quantities[i] else 0
                recipe_ingredient = RecipeIngredient(
                    quantity=quantity,
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id
                )
                db.session.add(recipe_ingredient)
        
        db.session.commit()
        
        flash('Рецепт успешно добавлен!', 'success')
        return redirect(url_for('recipes'))
    
    return render_template('add_recipe.html')

@app.route('/add_comment/<int:recipe_id>', methods=['POST'])
@login_required
def add_comment(recipe_id):
    content = request.form['content']
    
    comment = Comment(
        content=content,
        user_id=session['user_id'],
        recipe_id=recipe_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Комментарий добавлен!', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    recipes = [fav.recipe for fav in favorites]
    return render_template('favorites.html', recipes=recipes)

@app.route('/my_recipes')
@login_required
def my_recipes():
    recipes = Recipe.query.filter_by(user_id=session['user_id']).order_by(Recipe.created_at.desc()).all()
    return render_template('my_recipes.html', recipes=recipes)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    try:
        # Проверяем, что рецепт принадлежит текущему пользователю
        recipe = Recipe.query.filter_by(id=recipe_id, user_id=session['user_id']).first()
        
        if not recipe:
            return jsonify({'success': False, 'message': 'Рецепт не найден или у вас нет прав на его удаление'})
        
        # Удаляем связанные данные
        # Удаляем ингредиенты рецепта
        RecipeIngredient.query.filter_by(recipe_id=recipe_id).delete()
        
        # Удаляем комментарии
        Comment.query.filter_by(recipe_id=recipe_id).delete()
        
        # Удаляем оценки
        Rating.query.filter_by(recipe_id=recipe_id).delete()
        
        # Удаляем из избранного
        Favorite.query.filter_by(recipe_id=recipe_id).delete()
        
        # Удаляем изображение, если оно есть
        if recipe.image_path:
            import os
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], recipe.image_path)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except OSError:
                    pass  # Игнорируем ошибки при удалении файла
        
        # Удаляем сам рецепт
        db.session.delete(recipe)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Рецепт успешно удален'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/add_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def add_favorite(recipe_id):
    # Проверяем, не добавлен ли уже рецепт в избранное
    existing_favorite = Favorite.query.filter_by(
        user_id=session['user_id'], 
        recipe_id=recipe_id
    ).first()
    
    if not existing_favorite:
        favorite = Favorite(
            user_id=session['user_id'],
            recipe_id=recipe_id
        )
        db.session.add(favorite)
        db.session.commit()
        flash('Рецепт добавлен в избранное!', 'success')
    else:
        flash('Рецепт уже в избранном!', 'info')
    
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/remove_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favorite(recipe_id):
    favorite = Favorite.query.filter_by(
        user_id=session['user_id'], 
        recipe_id=recipe_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Рецепт удален из избранного!', 'info')
    
    return redirect(url_for('favorites'))

@app.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
    try:
        data = request.get_json()
        recipe_id = data.get('recipe_id')
        rating = data.get('rating')
        
        if not recipe_id or not rating:
            return jsonify({'success': False, 'message': 'Неверные данные'})
        
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Оценка должна быть от 1 до 5'})
        
        # Проверяем, есть ли уже оценка от этого пользователя
        existing_rating = Rating.query.filter_by(
            user_id=session['user_id'],
            recipe_id=recipe_id
        ).first()
        
        if existing_rating:
            # Обновляем существующую оценку
            existing_rating.rating = rating
        else:
            # Создаем новую оценку
            new_rating = Rating(
                user_id=session['user_id'],
                recipe_id=recipe_id,
                rating=rating
            )
            db.session.add(new_rating)
        
        db.session.commit()
        
        # Вычисляем среднюю оценку
        recipe_ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
        if recipe_ratings:
            average_rating = sum(r.rating for r in recipe_ratings) / len(recipe_ratings)
            total_ratings = len(recipe_ratings)
        else:
            average_rating = 0
            total_ratings = 0
        
        return jsonify({
            'success': True,
            'average_rating': average_rating,
            'total_ratings': total_ratings
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
