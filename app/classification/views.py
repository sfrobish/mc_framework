from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import classification
from .forms import ClassificationForm
from .. import db
from ..models import domain_dim as domaindbo
from ..models import geography_dim as geographydbo
from ..models import source_dim as sourcedbo
from ..models import usage_dim as usagedbo
  

@classification.route('/classification', methods=['GET', 'POST'])
def start_new_classification():
  
  # List all controls
  domainlist = domaindbo.query.order_by(asc(domaindbo.domain_name)).all()
  geographylist = geographydbo.query.order_by(asc(geographydbo.geo_name)).all()
  sourcelist = sourcedbo.query.order_by(asc(sourcedbo.source_name)).all()
  usagelist = usagedbo.query.order_by(asc(usagedbo.usage_name)).all()


  return render_template('classification/classification_multitab_template.html',
                           domainlist=domainlist,
                           geographylist=geographylist,
                           sourcelist=sourcelist,
                           usagelist=usagelist,
                           title="Get Classification")


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
