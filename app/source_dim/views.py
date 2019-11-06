from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import source_dim
from .forms import SourceForm
from .. import db
from ..models import source_dim as sourcedbo
  

@source_dim.route('/sources', methods=['GET', 'POST'])
def list_source_dims():
  
  # List all source_dims
  sourcelist = sourcedbo.query.order_by(asc(sourcedbo.source_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(sourcelist)
  pagination_sources = sourcelist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('source_dim/source_template.html',
                           source_dims=pagination_sources,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Source_Dims")


@source_dim.route('/sources/add', methods=['GET', 'POST'])
def add_source_dim():
  # Add a source_dim to the database

  add_source_dim = True

  form = SourceForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  sourcedata = sourcedbo(source_name=form.name.data,
                         source_descr=form.description.data,
                         parent_source_id=form.parent_id.data,
                         similarity_score=form.score.data)
  try:
    # add source_dim to the database
    db.session.add(sourcedata)
    db.session.commit()
    flash('You have successfully added a new source.')
  except:
    # in case source_dim name already exists
    flash('Error: source name already exists.')
  
  # redirect to source_dims page
  return redirect(url_for('source_dim.list_sources'))


@source_dim.route('/sources/edit/<int:id>', methods=['GET', 'POST'])
def edit_source_dim(id):

  # Edit a source_dim
  add_source_dim = False

  sourcedata = sourcedbo.query.get_or_404(id)
  form = SourceForm(obj=sourcedata)
  #if form.validate_on_submit():
  sourcedata.source_name = form.name.data
  sourcedata.source_descr = form.description.data
  sourcedata.parent_source_id = form.parent_id.data
  sourcedata.similarity_score = form.score.data
  db.session.commit()
  flash('You have successfully edited the source.')

  # redirect to the departments page
  return redirect(url_for('source_dim.list_sources'))


@source_dim.route('/sources/delete/<int:id>', methods=['GET', 'POST'])
def delete_source_dim(id):

  # Delete a source_dim from the database

  sourcedata = sourcedbo.query.get_or_404(id)
  db.session.delete(sourcedata)
  db.session.commit()
  flash('You have successfully deleted the source_dim.')

  # redirect to the source_dims page
  return redirect(url_for('source_dim.list_sources'))
