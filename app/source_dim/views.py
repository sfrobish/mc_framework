from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import source_dim
from .forms import Source_DimForm
from .. import db
from ..models import source_dim as source_dimdbo
  

@source_dim.route('/source_dims', methods=['GET', 'POST'])
def list_source_dims():
  
  # List all source_dims
  source_dimslist = source_dimdbo.query.order_by(asc(source_dimdbo.source_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(source_dimslist)
  pagination_source_dims = source_dimslist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('source_dim/crud_template.html',
                           source_dims=pagination_source_dims,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Source_Dims")


@source_dim.route('/source_dims/add', methods=['GET', 'POST'])
def add_source_dim():
  # Add a source_dim to the database

  add_source_dim = True

  form = Source_DimForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  cntldata = source_dimdbo(source_name=form.name.data,
                        source_descr=form.description.data,
                        parent_source_id=form.parent_id.data,
                        similarity_score=form.score.data)
  try:
    # add source_dim to the database
    db.session.add(cntldata)
    db.session.commit()
    flash('You have successfully added a new source.')
  except:
    # in case source_dim name already exists
    flash('Error: source name already exists.')
  
  # redirect to source_dims page
  return redirect(url_for('source_dim.list_source_dims'))


@source_dim.route('/source_dims/edit/<int:id>', methods=['GET', 'POST'])
def edit_source_dim(id):

  # Edit a source_dim
  add_source_dim = False

  cntldata = source_dimdbo.query.get_or_404(id)
  form = Source_DimForm(obj=cntldata)
  #if form.validate_on_submit():
  cntldata.source_name = form.name.data
  cntldata.source_descr = form.description.data
  db.session.commit()
  flash('You have successfully edited the source.')

  # redirect to the departments page
  return redirect(url_for('source_dim.list_source_dims'))

  form.description.data = cntldata.source_descr
  form.name.data = cntldata.source_name
  return render_template('source_dim/source_dim.html', action="Edit",
                         add_source_dim=add_source_dim, form=form,
                         source_dim=cntldata, title="Edit Source_Dim")


@source_dim.route('/source_dims/delete/<int:id>', methods=['GET', 'POST'])
def delete_source_dim(id):

  # Delete a source_dim from the database

  cntldata = source_dimdbo.query.get_or_404(id)
  db.session.delete(cntldata)
  db.session.commit()
  flash('You have successfully deleted the source_dim.')

  # redirect to the source_dims page
  return redirect(url_for('source_dim.list_source_dims'))

  return render_template(title="Delete source_dim")