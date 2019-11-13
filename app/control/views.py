from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json
from flask_login import login_required

from . import control
from .forms import ControlForm
from .. import db
from ..models import control as controldbo
from ..helpers import check_admin

@control.route('/controls', methods=['GET', 'POST'])
@login_required
def list_controls():
  
  check_admin()
  
  # List all controls
  controlslist = controldbo.query.order_by(asc(controldbo.control_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(controlslist)
  pagination_controls = controlslist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('control/control_template.html',
                           controls=pagination_controls,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Controls")


@control.route('/controls/add', methods=['GET', 'POST'])
@login_required
def add_control():
  # Add a control to the database

  check_admin()

  add_control = True

  form = ControlForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  cntldata = controldbo(control_name=form.name.data,
                        control_description=form.description.data)
  try:
    # add control to the database
    db.session.add(cntldata)
    db.session.commit()
    flash('You have successfully added a new control.')
  except:
    # in case control name already exists
    flash('Error: control name already exists.')
  
  # redirect to controls page
  return redirect(url_for('control.list_controls'))


@control.route('/controls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_control(id):

  check_admin()

  # Edit a control
  add_control = False

  cntldata = controldbo.query.get_or_404(id)
  form = ControlForm(obj=cntldata)
  #if form.validate_on_submit():
  cntldata.control_name = form.name.data
  cntldata.control_description = form.description.data
  db.session.commit()
  flash('You have successfully edited the control.')

  # redirect to the departments page
  return redirect(url_for('control.list_controls'))

  #form.description.data = cntldata.control_description
  #form.name.data = cntldata.control_name
  #return render_template('control/control.html', action="Edit",
  #                        add_control=add_control, form=form,
  #                        control=cntldata, title="Edit Control")


@control.route('/controls/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_control(id):

  check_admin()

  # Delete a control from the database

  cntldata = controldbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the control.')

  # redirect to the controls page
  return redirect(url_for('control.list_controls'))

  return render_template(title="Delete control")
