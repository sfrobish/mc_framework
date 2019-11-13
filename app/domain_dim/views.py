from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json
from flask_login import login_required

from . import domain
from .forms import DomainForm
from .. import db
from ..models import domain_dim as domaindbo
from ..helpers import check_admin
  
@domain.route('/domains', methods=['GET', 'POST'])
@login_required
def list_domains():

  check_admin()

  #List all domains
  domainslist = domaindbo.query.order_by(asc(domaindbo.domain_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(domainslist)
  pagination_domains = domainslist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

  return render_template('domain_dim/domain_template.html',
                          domainlist=pagination_domains,
                          pagination=pagination,
                          page=page,
                          per_page=per_page,
                          title="Domains")

@domain.route('/domains/add', methods=['GET', 'POST'])
@login_required
def add_domain():
  # Add a domain to the database

  check_admin()

  add_domain = True

  form = GeographyForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  
  
  print(form.name.data)
  domaindata = domaindbo(geo_name=form.name.data,
                         geo_descr=form.description.data,
                         parent_geo_id=form.parent.data,
                         similarity_score=form.similarity.data)
  try:
    # add domain to the database
    db.session.add(domaindata)
    db.session.commit()
    flash('You have successfully added a new domain.')
  except:
    # in case domain name already exists
    flash('Error: domain name already exists.')
  
  # redirect to domain page
  return redirect(url_for('domain.list_domains'))


@domain.route('/domains/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_domain(id):

  check_admin()

  print("made it " + str(id))
  # Edit a domain
  add_domain = False

  domaindata = domaindbo.query.get_or_404(id)
  
  form = GeographyForm(obj=domaindata)
  #if form.validate_on_submit():
  domaindata.geo_name = form.name.data
  domaindata.geo_descr = form.description.data
  domaindata.parent_geo_id = form.parent.data
  domaindata.similarity_score = form.similarity.data
  db.session.commit()
  flash('You have successfully edited the domain.')

  # redirect to the departments page
  return redirect(url_for('domain.list_domains'))


@domain.route('/domains/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_domain(id):

  check_admin()

  # Delete a domain from the database
  print(id)
  domaindata = domaindbo.query.get_or_404(id)
  db.session.delete(domaindata)
  db.session.commit()
  flash('You have successfully deleted the domain.')

  # redirect to the domain page
  return redirect(url_for('domain.list_domains'))
