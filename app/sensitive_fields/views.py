from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json
from flask_login import login_required

from . import sdf_dim
from .forms import SensitiveFieldsForm
from .. import db
from ..models import sdf_dim as sdfdbo
from ..helpers import check_admin
  

@sdf_dim.route('/sensitive-fields', methods=['GET', 'POST'])
@login_required
def list_sensitive_fields():

  check_admin()
  
  # List all sdf_dims
  sdflist = sdfdbo.query.order_by(asc(sdfdbo.sdf_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(sdflist)
  pagination_sdfs = sdflist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('sensitive_fields/sensitive_fields_template.html',
                           sdf_dims=pagination_sdfs,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Source_Dims")


@sdf_dim.route('/sensitive-fields/add', methods=['GET', 'POST'])
@login_required
def add_sdf_dim():

  check_admin()

  # Add a sdf_dim to the database

  add_sdf_dim = True

  form = SensitiveFieldsForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  sdfdata = sdfdbo(sdf_name=form.name.data,
                   sdf_descr=form.description.data,
                   sdf_regex=form.regex.data,
                   risk_score=form.score.data)
  try:
    # add sdf_dim to the database
    db.session.add(sdfdata)
    db.session.commit()
    flash('You have successfully added a new sdf.')
  except:
    # in case sdf_dim name already exists
    flash('Error: sdf name already exists.')
  
  # redirect to sdf_dims page
  return redirect(url_for('sdf_dim.list_sensitive_fields'))


@sdf_dim.route('/sensitive-fields/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sdf_dim(id):

  check_admin()

  # Edit a sdf_dim
  add_sdf_dim = False

  sdfdata = sdfdbo.query.get_or_404(id)
  form = SensitiveFieldsForm(obj=sdfdata)
  print(dir(form))
  print(form.regex.data)
  #if form.validate_on_submit():
  sdfdata.sdf_name = form.name.data
  sdfdata.sdf_descr = form.description.data
  sdfdata.sdf_regex = form.regex.data
  sdfdata.risk_score = form.score.data
  db.session.commit()
  flash('You have successfully edited the sdf.')

  # redirect to the departments page
  return redirect(url_for('sdf_dim.list_sensitive_fields'))


@sdf_dim.route('/sensitive-fields/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_sdf_dim(id):

  check_admin()

  # Delete a sdf_dim from the database

  sdfdata = sdfdbo.query.get_or_404(id)
  db.session.delete(sdfdata)
  db.session.commit()
  flash('You have successfully deleted the sdf_dim.')

  # redirect to the sdf_dims page
  return redirect(url_for('sdf_dim.list_sensitive_fields'))
