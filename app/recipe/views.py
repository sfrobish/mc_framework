from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import recipe
from .forms import RecipeForm
from .. import db
from ..models import recipe as recipedbo
from ..models import control as controldbo
from ..models import control_recipe as controlrecipedbo
  

@recipe.route('/recipes', methods=['GET', 'POST'])
def list_recipes():
  
  # List all recipes
  recipeslist = recipedbo.query.order_by(asc(recipedbo.recipe_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(recipeslist)
  pagination_recipes = recipeslist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

  return render_template('recipe/recipe_template.html',
                           recipelist=pagination_recipes,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Controls")


@recipe.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
  # Add a recipe to the database

  add_recipe = True

  form = RecipeForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  recipedata = recipedbo(recipe_name=form.name.data,
                        recipe_description=form.description.data)
  try:
    # add recipe to the database
    db.session.add(cntldata)
    db.session.commit()
    flash('You have successfully added a new recipe.')
  except:
    # in case recipe name already exists
    flash('Error: recipe name already exists.')
  
  # redirect to recipes page
  return redirect(url_for('recipe.list_recipes'))

@recipe.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):

  # Edit a department
  add_recipe = False

  recipedata = recipedbo.query.get_or_404(id)
  form = RecipeForm(obj=recipedata)
  #if form.validate_on_submit():
  recipedata.recipe_name = form.name.data
  recipedata.recipe_description = form.description.data
  db.session.commit()
  flash('You have successfully edited the recipe.')

  # redirect to the departments page
  return redirect(url_for('recipe.list_recipes'))


@recipe.route('/recipes/delete/<int:id>', methods=['GET', 'POST'])
def delete_recipe(id):

  # Delete a department from the database

  recipedata = recipedbo.query.get_or_404(id)
  db.session.delete(recipedata)
  db.session.commit()
  flash('You have successfully deleted the recipe.')

    # redirect to the departments page
  return redirect(url_for('recipe.list_recipes'))
