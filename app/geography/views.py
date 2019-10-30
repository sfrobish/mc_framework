from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import geography
from .forms import GeographyForm
from .. import db
from ..models import geography as geographydbo
  

@geography.route('/geography', methods=['GET', 'POST'])
def list_geography():
  
  # List all geography
  geographylist = geographydbo.query.order_by(asc(geographydbo.geo_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(geographylist)
  pagination_geography = geographylist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('geography/geography_template.html',
                           geography=pagination_geography,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="geography")


@geography.route('/geography/add', methods=['GET', 'POST'])
def add_geography():
  # Add a geography to the database

  add_geography = True

  form = GeographyForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  
  
  print(form.name.data)
  geodata = geographydbo(geo_name=form.name.data,
                        geo_descr=form.description.data,
                        parent_geo_id=form.parent.data,
                        similarity_score=form.similarity.data)
  try:
    # add geography to the database
    db.session.add(geodata)
    db.session.commit()
    flash('You have successfully added a new geography.')
  except:
    # in case geography name already exists
    flash('Error: geography name already exists.')
  
  # redirect to geography page
  return redirect(url_for('geography.list_geography'))


@geography.route('/geography/edit/<int:id>', methods=['GET', 'POST'])
def edit_geography(id):

  # Edit a geography
  add_geography = False

  geodata = geographydbo.query.get_or_404(id)
  form = GeographyForm(obj=geodata)
  #if form.validate_on_submit():
  geodata.geo_name = form.name.data
  geodata.geo_descr = form.description.data
  geodata.parent_geo_id = form.parent.data
  geodata.similarity_score=form.similarity.data
  db.session.commit()
  flash('You have successfully edited the geography.')

  # redirect to the departments page
  return redirect(url_for('geography.list_geography'))

  #form.description.data = geodata.geo_descr
  #form.name.data = geodata.geo_name
  #return render_template('geography/geography.html', action="Edit",
  #                        add_geography=add_geography, form=form,
  #                        geography=geodata, title="Edit geography")


@geography.route('/geography/delete/<int:id>', methods=['GET', 'POST'])
def delete_geography(id):

  # Delete a geography from the database
  print(id)
  geodata = geographydbo.query.get_or_404(id)
  db.session.delete(geodata)
  db.session.commit()
  flash('You have successfully deleted the geography.')

  # redirect to the geography page
  return redirect(url_for('geography.list_geography'))

  return render_template(title="Delete geography")