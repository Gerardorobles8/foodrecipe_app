from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RecipeForm, LoginForm, DeleteForm
from app.models import Recipe, User
from app import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/recipes')
def list_recipes():
    recipes = Recipe.query.all()
    return render_template('recipe_list.html', recipes=recipes)

@main.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            author=current_user  # Link to logged-in user
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe created successfully!')
        return redirect(url_for('main.list_recipes'))
    return render_template('recipe_form.html', form=form)

@main.route('/recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = DeleteForm()
    return render_template('recipe_detail.html', recipe=recipe, form=form)

@main.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!')
    return redirect(url_for('main.list_recipes'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # TEMP (plaintext password)
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.list_recipes'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.list_recipes'))
