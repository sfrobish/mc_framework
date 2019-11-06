from flask import abort, flash, redirect, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
import json

from . import contract
from .forms import ContractForm
from .. import db
from ..models import contract_dim as contractdbo
  

@contract.route('/contracts', methods=['GET', 'POST'])
def list_contracts():
  
  # List all contracts
  contractslist = contractdbo.query.order_by(asc(contractdbo.contract_name)).all()

  page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
  total = len(contractslist)
  pagination_contracts = contractslist[offset: offset + per_page]
  pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


  return render_template('contract_dim/contract_template.html',
                           contracts=pagination_contracts,
                           pagination=pagination,
                           page=page,
                           per_page=per_page,
                           title="Contracts")


@contract.route('/contracts/add', methods=['GET', 'POST'])
def add_contract():
  # Add a contract to the database

  add_contract = True

  form = ContractForm()
  """   if form.is_submitted:
    print("Submitted")
  if form.validate():
    print("VALID ONE")
  print(form.errors)
  if form.validate_on_submit():
    print("VALID") """
  contractdata = contractdbo(contract_name=form.name.data,
                             contract_description=form.description.data,
                             parent_contract_id=form.parent.data,
                             similarity_score=form.similarity.data)
  try:
    # add contract to the database
    db.session.add(contractdata)
    db.session.commit()
    flash('You have successfully added a new contract.')
  except:
    # in case contract name already exists
    flash('Error: contract name already exists.')
  
  # redirect to contracts page
  return redirect(url_for('contract.list_contracts'))


@contract.route('/contracts/edit/<int:id>', methods=['GET', 'POST'])
def edit_contract(id):

  # Edit a contract
  add_contract = False

  contractdata = contractdbo.query.get_or_404(id)
  form = ContractForm(obj=contractdata)
  #if form.validate_on_submit():
  contractdata.contract_name = form.name.data
  contractdata.contract_description = form.description.data
  db.session.commit()
  flash('You have successfully edited the control.')

  # redirect to the departments page
  return redirect(url_for('contract.list_contracts'))


@contract.route('/contracts/delete/<int:id>', methods=['GET', 'POST'])
def delete_contract(id):

  # Delete a contract from the database

  contractdata = contractdbo.query.get_or_404(id)
  db.session.delete(contractdata)
  db.session.commit()
  flash('You have successfully deleted the contract.')

  # redirect to the contracts page
  return redirect(url_for('contract.list_contracts'))
