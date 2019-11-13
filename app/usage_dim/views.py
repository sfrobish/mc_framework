from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json
from flask_login import login_required

from . import usage
from .forms import UsageForm
from .. import db
from ..models import usage_dim as usagedbo
from ..helpers import confirm_user_is_admin
  

@usage.route('/usages', methods=['GET', 'POST'])
@login_required
def list_usage():

  confirm_user_is_admin()
  
  # List all usages
  usagelist = usagedbo.query.order_by(asc(usagedbo.usage_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(usagelist)
  pagination_usage = usagelist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('usage_dim/usage_template.html',
                           usages=pagination_usage,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Usage")


@usage.route('/usages/add', methods=['GET', 'POST'])
@login_required
def add_usage():

  confirm_user_is_admin()

  # Add a usage to the database

  add_usage = True

  form = UsageForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  usagedata = usagedbo(usage_name=form.name.data,
                       usage_descr=form.description.data,
                       parent_usage_id=form.parent_id.data,
                       similarity_score=form.score.data)
  try:
    # add usage to the database
    db.session.add(usagedata)
    db.session.commit()
    flash('You have successfully added a new usage.')
  except:
    # in case usage name already exists
    flash('Error: usage name already exists.')
  
  # redirect to usage page
  return redirect(url_for('usage.list_usage'))


@usage.route('/usages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_usage(id):

  confirm_user_is_admin()

  # Edit a usage
  add_usage = False

  usagedata = usagedbo.query.get_or_404(id)
  form = UsageForm(obj=usagedata)
  #if form.validate_on_submit():
  usagedata.usage_name = form.name.data
  usagedata.usage_descr = form.description.data
  usagedata.parent_usage_id = form.parent_id.data
  usagedata.similarity_score = form.score.data
  db.session.commit()
  flash('You have successfully edited the usage.')

  # redirect to the usage list page
  return redirect(url_for('usage.list_usage'))


@usage.route('/usages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_usage(id):

  confirm_user_is_admin()

  # Delete a usage from the database

  cntldata = usagedbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the usage.')

  # redirect to the usage page
  return redirect(url_for('usage.list_usage'))
