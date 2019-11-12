from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import ident_dim
from .forms import IdentifiabilityForm
from .. import db
from ..models import ident_dim as identdbo
from ..models import sdf_dim as sdfdbo
  

@ident_dim.route('/identifiability', methods=['GET', 'POST'])
def list_ident_rules():
  
  # List all ident_dims with Sensitive field names
  sql = "select array_agg(f.sdf_name) as field_list, i.rule_id, i.risk_score, i.risk_type \
        from mc_demo.identifiability_rules i \
        left join mc_demo.sensitive_data_fields f \
        on f.sdf_id = any(i.field_id_list) \
        group by i.rule_id"
  result = db.engine.execute(sql)
  print(result)
  identlist = [row for row in result]
  print(identlist)

  # Sensitive data fields for populating the selectpicker
  sdflist = sdfdbo.query.order_by(asc(sdfdbo.sdf_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(identlist)
  pagination_idents = identlist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('identifiability/identifiability_template.html',
                           ident_dims=pagination_idents,
                           sdf_dims=sdflist,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Identifiability Rules")


@ident_dim.route('/identifiability/add', methods=['GET', 'POST'])
def add_ident_dim():
  # Add a ident_dim to the database

  add_ident_dim = True

  form = IdentifiabilityForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  identdata = identdbo(risk_type=form.risk_type.data,
                       risk_score=form.risk_score.data,
                       field_list=form.sdfpicker.data)

  try:
    # add ident_dim to the database
    db.session.add(identdata)
    db.session.commit()
    flash('You have successfully added a new ident.')
  except:
    # in case ident_dim name already exists
    flash('Error: ident name already exists.')
  
  # redirect to ident_dims page
  return redirect(url_for('ident_dim.list_ident_rules'))


@ident_dim.route('/identifiability/edit/<int:id>', methods=['GET', 'POST'])
def edit_ident_dim(id):

  # Edit a ident_dim
  add_ident_dim = False

  identdata = identdbo.query.get_or_404(id)
  form = IdentifiabilityForm(obj=identdata)
  #if form.validate_on_submit():
  identdata.risk_type = form.risk_type.data
  identdata.risk_score = form.risk_score.data
  identdata.field_list = form.sdfpicker.data
  
  db.session.commit()
  flash('You have successfully edited the sdf.')

  # redirect to the departments page
  return redirect(url_for('ident_dim.list_ident_rules'))


@ident_dim.route('/identifiability/delete/<int:id>', methods=['GET', 'POST'])
def delete_ident_dim(id):

  # Delete a ident_dim from the database

  sdfdata = identdbo.query.get_or_404(id)
  db.session.delete(sdfdata)
  db.session.commit()
  flash('You have successfully deleted the ident_dim.')

  # redirect to the ident_dims page
  return redirect(url_for('ident_dim.list_ident_rules'))
