from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import domain_dim
from .forms import DomainForm
from .. import db
from ..models import domain_dim as domaindbo
  
@domain_dim.route('/domain_dim', methods=['GET', 'POST'])
def list_domain_dim():
    #List all domains
    domainslist = domaindbo.query.order_by(asc(domaindbo.domain_name)).all()

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(domainslist)
    pagination_controls = domainslist[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('domain_dim/crud_template.html',
                            domains=pagination_controls,
                            pagination=pagination,
                            page=page,
                            per_page=per_page,
                            title="Domains")

""" 

@control.route('/controls/add', methods=['GET', 'POST'])
def add_control():
  # Add a control to the database

  add_control = True

  form = ControlForm()
  """   
  


""" if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID")  """
    
    
"""
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
def edit_control(id):

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
def delete_control(id):

  # Delete a control from the database

  cntldata = controldbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the control.')

  # redirect to the controls page
  return redirect(url_for('control.list_controls'))

  return render_template(title="Delete control") """