from flask import abort, flash, redirect, render_template, url_for
from sqlalchemy import text

from . import control_recipe
from .forms import ControlRecipeForm
from .. import db
from ..models import control as controldbo
from ..models import recipe as recipedbo
from ..models import control_recipe as controlrecipedbo


@control_recipe.route('/control_recipes', methods=['GET', 'POST'])
def list_control_recipes():
  
  # List all recipes
  sql = text("select cr.control_recipe_id, c.control_id, c.control_name, " +
                     " r.recipe_id, r.recipe_name " +
             "from mc_demo.control_recipe cr " +
             "inner join mc_demo.control c " +
             "  on cr.control_id = c.control_id " +
             "inner join mc_demo.recipe r " +
             "  on cr.recipe_id = r.recipe_id ")
  crlist = db.engine.execute(sql)

  return render_template("recipe/recipe_crud.html",
                         controlrecipes=crlist, title="Control Recipes")


@control_recipe.route('/control_recipes/add/<int:rid>/<int:cid>', methods=['GET', 'POST'])
def add_control_recipe(rid, cid):

  # Add a control recipe to the database

    add_control_recipe = True
    
    form = ControlRecipeForm()
    """   if form.is_submitted:
      print("Submitted")
    if form.validate():
      print("VALID ONE")
    print(form.errors)
    if form.validate_on_submit():
      print("VALID") """
    crdata = controlrecipedbo(control_id=cid, #form.control_id.data,
                              recipe_id=rid) #form.recipe_id.data)
    try:
      # add control recipe to the database
      db.session.add(crdata)
      db.session.commit()
      flash('You have successfully added a new control recipe.')
    except:
      # in case control recipe id already exists
      flash('Error: control recipe already exists.')
    
    # redirect to controls page
    return redirect(url_for('control_recipe.list_control_recipes'))

  # load control template
    # return render_template('recipe/recipe_crud.html', action="Add",
    #                       add_control_recipe=add_control_recipe, form=form,
    #                       title="Add Control Recipe")


@control_recipe.route('/control_recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit_control_recipe(id):

  # Edit a control recipe
  add_control_recipe = False

  crdata = controlrecipedbo.query.get_or_404(id)
  form = ControlRecipeForm(obj=crdata)
  # Load choices
  form.control.choices = [(c.control_id, c.control_name) for c in controldbo.query.order_by("control_name")]
  form.recipe.choices = [(r.recipe_id, r.recipe_name) for r in recipedbo.query.order_by("recipe_name")]
  if form.validate_on_submit():
    crdata.control_id = form.control.data
    crdata.recipe_id = form.recipe.data
    db.session.commit()
    flash('You have successfully edited the control.')

    # redirect to the control recipes page
    return redirect(url_for('control_recipe.list_control_recipes'))

  form.control.data = crdata.control_id
  form.recipe.data = crdata.recipe_id
  return render_template('control_recipe/control_recipe.html', action="Edit",
                          add_control_recipe=add_control_recipe, form=form,
                          control=crdata, title="Edit Control Recipe")


@control_recipe.route('/control_recipes/delete/<int:id>', methods=['GET', 'POST'])
def delete_control_recipe(id):

  # Delete a control recipe from the database

  crdata = controlrecipedbo.query.get_or_404(id)
  db.session.delete(crdata)
  db.session.commit()
  flash('You have successfully deleted the control recipe.')

  # redirect to the control recipes page
  return redirect(url_for('control_recipe.list_control_recipes'))

  return render_template(title="Delete control recipe")