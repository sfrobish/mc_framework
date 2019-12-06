from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError
import json
import re
import numpy
from flask_login import login_required

from . import classification
from .forms import ClassificationForm
from .. import db
from ..models import domain_dim as domaindbo
from ..models import geography_dim as geographydbo
from ..models import source_dim as sourcedbo
from ..models import usage_dim as usagedbo
from ..models import sdf_dim as sdfdbo
from ..models import ident_dim as identdbo
from ..models import submitted_forms as submitteddbo
from ..models import classification as classificationdbo
from ..helpers import get_nested_children

  

@classification.route('/classification', methods=['GET', 'POST'])
@login_required
def start_new_classification():
  
  domainlist = domaindbo.query.order_by(asc(domaindbo.domain_name)).all()
  geographylist = geographydbo.query.order_by(asc(geographydbo.geo_name)).all()
  nested_geographylist = get_nested_children(geographylist)
  sourcelist = sourcedbo.query.order_by(asc(sourcedbo.source_name)).all()
  usagelist = usagedbo.query.order_by(asc(usagedbo.usage_name)).all()
  sdflist = sdfdbo.query.order_by(asc(sdfdbo.sdf_name)).all()


  return render_template('classification/classification_multitab_template.html',
                           domainlist=domainlist,
                           geographylist=nested_geographylist,
                           sourcelist=sourcelist,
                           usagelist=usagelist,
                           sdflist=sdflist,
                           title="Get Classification")


def apply_regexes(fieldlist):

  sdflist = sdfdbo.query.all()
  
  sensitivefields = []
  for sdf in sdflist:
    patstr = sdf.sdf_regex
    try:
      pat = re.compile(patstr, re.IGNORECASE)
      sdfvalid = True
    except re.error:
      print("Pattern is not valid: " + patstr)
      sdfvalid = False
    if sdfvalid:
      for field in fieldlist:
        m = pat.search(field)
        if m is not None:
          sensitivefields.append(sdf.sdf_id)

  return sensitivefields


def find_ident_rules(sensitivefields):

  identrules = identdbo.query.all()

  sensitivefields.sort()

  foundrules = []
  for idrule in identrules:
    idrulelist = idrule.field_id_list
    idrulelist.sort()
    if all(x in sensitivefields for x in idrulelist):
      foundrules.append( ( idrule.rule_id , idrule.risk_score ) )

  return foundrules
    

def compare_submission(domainlist, geolist, sourcelist, usagelist, sdflist):

  if len(domainlist) == 0:
    domainscorelist = [ 0 ]
  else:
    domainscorelist = [ int(x.split("|")[1]) for x in domainlist ]
    domainscorelist.sort()
  if len(geolist) == 0:
    geoscorelist = [ 0 ]
  else:
    geoscorelist = [ int(x.split("|")[1]) for x in geolist ]
    geoscorelist.sort()
  if len(sourcelist) == 0:
    sourcescorelist = [ 0 ]
  else:
    sourcescorelist = [ int(x.split("|")[1]) for x in sourcelist ]
    sourcescorelist.sort()
  if len(usagelist) == 0:
    usagescorelist = [ 0 ]
  else:
    usagescorelist = [ int(x.split("|")[1]) for x in usagelist ]
    usagescorelist.sort()
  if len(sdflist) == 0:
    sdfscorelist = [ 0 ]
  else:
    sdfscorelist = [ int(x.split("|")[1]) for x in sdflist ]
    sdfscorelist.sort()

  classdict = { "domain"     : domainscorelist[-1],
                "geography"  : geoscorelist[-1],
                "source"     : sourcescorelist[-1],
                "usage"      : usagescorelist[-1],
                "field"      : sdfscorelist[-1]
              }

  print(json.dumps(classdict, indent=4))
  # Start simple with highest score of in the list used as coordinate
  subnpar = numpy.array([domainscorelist[-1],sourcescorelist[-1],geoscorelist[-1],usagescorelist[-1],sdfscorelist[-1]])

  allclass = classificationdbo.query.all()
  froblist = []
  for c in allclass:
    # Known domains
    kdomlist = c.domain_list
    if len(kdomlist) == 0:
      kdomlist = [0]
    else:
      kdomlist.sort()

    # Known sources
    ksrclist = c.source_list
    if len(ksrclist) == 0:
      ksrclist = [0]
    else:
      ksrclist.sort()

    # Known geographies
    kgeolist = c.geography_list
    if len(kgeolist) == 0:
      kgeolist = [0]
    else:
      kgeolist.sort()
    
    # Known usages
    kuselist = c.usage_list
    if len(kuselist) == 0:
      kuselist = [0]
    else:
      kuselist.sort()

    # Known identifiability rules
    kidrlist = c.field_list
    if len(kidrlist) == 0:
      kidrlist = [0]
    else:
      kidrlist.sort()

    # Build vector  
    knownnpar = numpy.array([kdomlist[-1],ksrclist[-1],kgeolist[-1],kuselist[-1],kidrlist[-1]])
    print(knownnpar)
    froblist.append( ( c.classification_id , numpy.linalg.norm(subnpar-knownnpar) ) )

  froblist.sort(key=lambda x: x[1])

  return froblist



@classification.route('/classification/submit', methods=['GET', 'POST'])
@login_required
def submit_classification():

  # Submit a new classification for evaluation

  submitobj = request.get_json()

  domainlist = submitobj["domain_list"]
  domainidlist = [ int(i.split("|")[0]) for i in domainlist ]
  domainidlist.sort()
  geolist = submitobj["geography_list"]
  geoidlist = [ int(i.split("|")[0]) for i in geolist ]
  geoidlist.sort()
  sourcelist = submitobj["source_list"]
  sourceidlist = [ int(i.split("|")[0]) for i in sourcelist ]
  sourceidlist.sort()
  usagelist = submitobj["usage_list"]
  usageidlist = [ int(i.split("|")[0]) for i in usagelist ]
  usageidlist.sort()
  sdflist = submitobj["sdf_list"]
  sdfidlist = [ int(i.split("|")[0]) for i in sdflist ]
  sdfidlist.sort()

  submitdata = submitteddbo(
                            domain_id_list=domainidlist,
                            source_id_list=sourceidlist,
                            geography_id_list=geoidlist,
                            usage_id_list=usageidlist,
                            field_id_list=sdfidlist,
                            rights_id_list=[],
                            contract_id_list=[]
                           )

  try:
    # add classification to the database
    db.session.add(submitdata)
    db.session.commit()
    print('You have successfully added a new classification.')
  except SQLAlchemyError as e:
    # in case classification already exists
    print(e)




  froblist = compare_submission(domainlist, geolist, sourcelist, usagelist, sdflist)
  
  print(json.dumps(froblist, indent=4))
  classdata = classificationdbo.query.get_or_404(froblist[0][0])
  sql = "select c.control_name || ' | ' || c.control_description \
           from mc_demo.control_recipe cr \
           left join mc_demo.control c \
           on cr.control_id = c.control_id \
           where cr.recipe_id = " + str(classdata.recipe_id)
  controlresult = db.engine.execute(sql)
  controllist = [ row[0] for row in controlresult ]
  if froblist[0][1] == 0:
    retdict = { "found" : True,
                "classid": classdata.classification_id,
                "control_list": controllist,
                "label": classdata.label
              }
  else:
    retdict = { "found" : False,
                "classid": classdata.classification_id,
                "recipeid": controllist,
                "label": classdata.label
              }

    
  return jsonify(retdict)


@classification.route('/classification/add', methods=['GET', 'POST'])
@login_required
def add_classification():
  
  submitobj = request.get_json()

  print(json.dumps(submitobj, indent=4))

  domainlist = submitobj["domain_list"]
  domainscorelist = [ int(i.split("|")[1]) for i in domainlist ]
  domainscorelist.sort()
  geolist = submitobj["geography_list"]
  geoscorelist = [ int(i.split("|")[1]) for i in geolist ]
  geoscorelist.sort()
  sourcelist = submitobj["source_list"]
  sourcescorelist = [ int(i.split("|")[1]) for i in sourcelist ]
  sourcescorelist.sort()
  usagelist = submitobj["usage_list"]
  usagescorelist = [ int(i.split("|")[1]) for i in usagelist ]
  usagescorelist.sort()
  sdflist = submitobj["sdf_list"]
  sdfscorelist = [ int(i.split("|")[1]) for i in sdflist ]
  sdfscorelist.sort()

  classid = submitobj["near_class_id"]
  classrow = classificationdbo.query.get_or_404(classid)


  newclass = classificationdbo(
                                domain_list=domainscorelist,
                                source_list=sourcescorelist,
                                geography_list=geoscorelist,
                                usage_list=usagescorelist,
                                field_list=sdfscorelist,
                                rights_list=[],
                                contract_list=[],
                                recipe_id=classrow.recipe_id,
                                label=classrow.label
                              )
  
  try:
    # add classification to the database
    db.session.add(newclass)
    db.session.commit()
    flash('You have successfully added a new classification.')
  except:
    # in case classification already exists
    flash('Error: classification already exists.')

  return url_for("home.homepage")
