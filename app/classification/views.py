from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import classification
from .forms import ClassificationForm
from .. import db
from ..models import classification as classificationdbo
  

@classification.route('/classfications', methods=['GET', 'POST'])
def list_classifications():
  
  # List all controls
  classificationlist = classificationdbo.query.order_by(asc(classificationdbo.label)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(classificationlist)
  pagination_classifications = classificationlist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('classification/classification_template.html',
                           classifications=pagination_classifications,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Classifications")


@classification.route('/classifications/add', methods=['GET', 'POST'])
def add_classification():
  # Add a classification to the database

  add_classification = True

  form = ClassificationForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  classificationdata = classificationdbo(control_name=form.name.data,
                        control_description=form.description.data)
  try:
    # add classification to the database
    db.session.add(classificationdata)
    db.session.commit()
    flash('You have successfully added a new classification.')
  except:
    # in case classification already exists
    flash('Error: classification already exists.')
  
  # redirect to classifications page
  return redirect(url_for('classification.list_classifications'))


@classification.route('/classifications/edit/<int:id>', methods=['GET', 'POST'])
def edit_classification(id):

  # Edit a classification
  add_classification = False

  classificationdata = classificationdbo.query.get_or_404(id)
  form = ClassificationForm(obj=classificationdata)
  #if form.validate_on_submit():
  classificationdata.control_name = form.name.data
  classificationdata.control_description = form.description.data
  db.session.commit()
  flash('You have successfully edited the classification.')

  # redirect to the departments page
  return redirect(url_for('classification.list_classifications'))


@classification.route('/classifications/delete/<int:id>', methods=['GET', 'POST'])
def delete_classification(id):

  # Delete a classification from the database

  classificationdata = classificationdbo.query.get_or_404(id)
  db.session.delete(classificationdata)
  db.session.commit()
  flash('You have successfully deleted the classification.')

  # redirect to the controls page
  return redirect(url_for('classification.list_classifications'))
