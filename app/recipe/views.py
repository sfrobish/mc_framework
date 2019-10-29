from flask import abort, flash, redirect, render_template, url_for

from . import recipe
from .forms import RecipeForm
from .. import db
from ..models import recipe as recipedbo
  

@recipe.route('/recipes', methods=['GET', 'POST'])
def list_recipes():
  
  # List all recipes
  recipeslist = recipedbo.query.all()

  return render_template('recipe/recipes.html',
                           recipes=recipeslist, title="Recipes")


@recipe.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
  # Add a recipe to the database

  add_recipe = True

  form = RecipeForm()
  if form.validate_on_submit():
    cntldata = recipedbo(recipe_name=form.name.data,
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

  # load recipe template
  return render_template('recipe/recipe.html', action="Add",
                          add_recipe=add_recipe, form=form,
                          title="Add Recipe")


@recipe.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):

  # Edit a department
  add_recipe = False

  cntldata = recipedbo.query.get_or_404(id)
  form = RecipeForm(obj=cntldata)
  if form.validate_on_submit():
    cntldata.recipe_name = form.name.data
    cntldata.recipe_description = form.description.data
    db.session.commit()
    flash('You have successfully edited the recipe.')

    # redirect to the departments page
    return redirect(url_for('recipe.list_recipes'))

  form.description.data = cntldata.recipe_description
  form.name.data = cntldata.recipe_name
  return render_template('recipe/recipe.html', action="Edit",
                          add_recipe=add_recipe, form=form,
                          recipe=cntldata, title="Edit Recipe")


@recipe.route('/recipes/delete/<int:id>', methods=['GET', 'POST'])
def delete_recipe(id):

  # Delete a department from the database

  cntldata = recipedbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the recipe.')

    # redirect to the departments page
  return redirect(url_for('recipe.list_recipes'))

  return render_template(title="Delete recipe")