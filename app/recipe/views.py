from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json
from flask_login import login_required

from . import recipe
from .forms import RecipeForm
from .. import db
from ..models import recipe as recipedbo
from ..models import control as controldbo
from ..models import control_recipe as controlrecipedbo
from ..helpers import confirm_user_is_admin


@recipe.route('/recipes', methods=['GET', 'POST'])
@login_required
def list_recipes():

  confirm_user_is_admin()

  sql = "select array_agg(c.control_name) as control_name_list, array_agg(c.control_id) as control_id_list, \
                r.recipe_id, r.recipe_name, r.recipe_description \
         from mc_demo.recipe r \
         left join mc_demo.control_recipe cr \
         on r.recipe_id = cr.recipe_id \
         left join mc_demo.control c \
         on cr.control_id = c.control_id \
         group by r.recipe_id"
  result = db.engine.execute(sql)
  recipelist = [ row for row in result ]
  
  # List all controls for filling modals
  controlslist = controldbo.query.order_by(asc(controldbo.control_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(recipelist)
  pagination_recipes = recipelist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

  return render_template('recipe/recipe_template.html',
                           recipelist=pagination_recipes,
                           controlslist=controlslist,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Recipes")


@recipe.route('/recipes/add', methods=['GET', 'POST'])
@login_required
def add_recipe():

  confirm_user_is_admin()

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
@login_required
def edit_recipe(id):

  confirm_user_is_admin()

  # Edit a department
  add_recipe = False

  recipedata = recipedbo.query.get_or_404(id)

  form = RecipeForm(obj=recipedata)
  recipedict = request.json

  recipedata.recipe_name = recipedict["recipe_name"]
  recipedata.recipe_description = recipedict["recipe_desc"]

  recipedict["control_list"] = [ int(x) for x in recipedict["control_list"] ]
  
  # See if there is a change in controls
  sql = "select c.recipe_id, array_agg(c.control_id) as control_id_list \
         from mc_demo.control_recipe c \
         where c.recipe_id = " + str(id) + " \
         group by c.recipe_id"
  print(sql)
  result = db.engine.execute(sql)    
  curcontrollist = [ row[1] for row in result ]
  print(recipedict["control_list"])
  print(curcontrollist)
  if len(curcontrollist) == 0:
    curcontrollist = [ [] ]
  if curcontrollist[0] == recipedict["control_list"]:
    print("No change to control list")
  else:
    # Delete all of the current controls in recipe
    delsql = "delete from mc_demo.control_recipe where recipe_id = " + str(id)
    db.engine.execute(delsql)

    # Insert new controllist
    for ctl in recipedict["control_list"]:
      insql = "insert into mc_demo.control_recipe (recipe_id, control_id) values (" + str(id) + "," + str(ctl) + ")"
      print(insql)
      db.engine.execute(insql)

  db.session.commit()
  flash('You have successfully edited the recipe.')

  # redirect to the departments page
  return redirect(url_for('recipe.list_recipes'))


@recipe.route('/recipes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):

  confirm_user_is_admin()

  # Delete a department from the database

  recipedata = recipedbo.query.get_or_404(id)
  db.session.delete(recipedata)
  db.session.commit()
  flash('You have successfully deleted the recipe.')

    # redirect to the departments page
  return redirect(url_for('recipe.list_recipes'))
