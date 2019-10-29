from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import usage
from .forms import UsageForm
from .. import db
from ..models import usage as usagedbo
  

@usage.route('/usage', methods=['GET', 'POST'])
def list_usage():
  
  # List all usages
  usagelist = usagedbo.query.order_by(asc(usagedbo.usage_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(usagelist)
  pagination_usage = usagelist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('usage/usage_template.html',
                           usage=pagination_usage,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Usage")


@usage.route('/usage/add', methods=['GET', 'POST'])
def add_usage():
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
  cntldata = usagedbo(usage_name=form.name.data,
                        usage_description=form.description.data)
  try:
    # add usage to the database
    db.session.add(cntldata)
    db.session.commit()
    flash('You have successfully added a new usage.')
  except:
    # in case usage name already exists
    flash('Error: usage name already exists.')
  
  # redirect to usage page
  return redirect(url_for('usage.list_usage'))


@usage.route('/usage/edit/<int:id>', methods=['GET', 'POST'])
def edit_usage(id):

  # Edit a usage
  add_usage = False

  cntldata = usagedbo.query.get_or_404(id)
  form = UsageForm(obj=cntldata)
  #if form.validate_on_submit():
  cntldata.usage_name = form.name.data
  cntldata.usage_description = form.description.data
  cntldata.usage_parent = form.parent.data
  cntldata.parent_usage_id = form.parent_usage_id.data
  cntldata.usage_similarity_score = form.usage_similarity_score
  db.session.commit()
  flash('You have successfully edited the usage.')

  # redirect to the departments page
  return redirect(url_for('usage.list_usage'))

  #form.description.data = cntldata.control_description
  #form.name.data = cntldata.control_name
  #return render_template('control/control.html', action="Edit",
  #                        add_control=add_control, form=form,
  #                        control=cntldata, title="Edit Control")


@usage.route('/usage/delete/<int:id>', methods=['GET', 'POST'])
def delete_usage(id):

  # Delete a usage from the database

  cntldata = usagedbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the usage.')

  # redirect to the usage page
  return redirect(url_for('usage.list_usage'))

  return render_template(title="Delete usage")