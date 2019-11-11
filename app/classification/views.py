from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_paginate import Pagination, get_page_args
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError
import json
import re
import numpy

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

  

@classification.route('/classification', methods=['GET', 'POST'])
def start_new_classification():
  
  domainlist = domaindbo.query.order_by(asc(domaindbo.domain_name)).all()
  geographylist = geographydbo.query.order_by(asc(geographydbo.geo_name)).all()
  sourcelist = sourcedbo.query.order_by(asc(sourcedbo.source_name)).all()
  usagelist = usagedbo.query.order_by(asc(usagedbo.usage_name)).all()


  return render_template('classification/classification_multitab_template.html',
                           domainlist=domainlist,
                           geographylist=geographylist,
                           sourcelist=sourcelist,
                           usagelist=usagelist,
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
    

def compare_submission(domainlist, geolist, sourcelist, usagelist, identruleslist):

  domainscorelist = [ int(x.split("|")[1]) for x in domainlist ]
  domainscorelist.sort()
  geoscorelist = [ int(x.split("|")[1]) for x in geolist ]
  geoscorelist.sort()
  sourcescorelist = [ int(x.split("|")[1]) for x in sourcelist ]
  sourcescorelist.sort()
  usagescorelist = [ int(x.split("|")[1]) for x in usagelist ]
  usagescorelist.sort()
  identscorelist = [ x[1] for x in identruleslist ]
  identscorelist.sort()

  classdict = { "domain"          : domainscorelist[-1],
                "geography"       : geoscorelist[-1],
                "source"          : sourcescorelist[-1],
                "usage"           : usagescorelist[-1],
                "identifiability" : identscorelist[-1]
              }

  print(json.dumps(classdict, indent=4))
  # Start simple with highest score of in the list used as coordinate
  subnpar = numpy.array([domainscorelist[-1],sourcescorelist[-1],geoscorelist[-1],usagescorelist[-1],identscorelist[-1]])

  allclass = classificationdbo.query.all()
  froblist = []
  for c in allclass:
    kdomlist = c.domain_list
    kdomlist.sort()
    ksrclist = c.source_list
    ksrclist.sort()
    kgeolist = c.geography_list
    kgeolist.sort()
    kuselist = c.usage_list
    kuselist.sort()
    kidrlist = c.identifiability_rule_list
    kidrlist.sort()
    knownnpar = numpy.array([kdomlist[-1],ksrclist[-1],kgeolist[-1],kuselist[-1],kidrlist[-1]])
    print(knownnpar)
    froblist.append( ( c.classification_id , numpy.linalg.norm(subnpar-knownnpar) ) )

  froblist.sort(key=lambda x: x[1])

  return froblist



@classification.route('/classification/submit', methods=['GET', 'POST'])
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

  fields = submitobj["fields_string"]
  fieldlist = []
  if ("," in fields):
    fieldlist = fields.split(",")
  elif ("|" in fields):
    fieldlist = fields.split("|")
  elif ("\t" in fields):
    fieldlist = fields.split("\t")
  else:
    # Must be a single field
    fieldlist = [ fields ]
  
  sensitivefields = apply_regexes(fieldlist)
  identruleslist = find_ident_rules(sensitivefields)
  identrulesidlist = [ i[0] for i in identruleslist ]
  identrulesidlist.sort()

  submitdata = submitteddbo(
                            domain_id_list=domainidlist,
                            source_id_list=sourceidlist,
                            geography_id_list=geoidlist,
                            usage_id_list=usageidlist,
                            identifiability_rule_id_list=identrulesidlist,
                            rights_id_list=[],
                            contract_id_list=[]
                           )

  # try:
  #   # add classification to the database
  #   db.session.add(submitdata)
  #   db.session.commit()
  #   print('You have successfully added a new classification.')
  # except SQLAlchemyError as e:
  #   # in case classification already exists
  #   print(e)




  froblist = compare_submission(domainlist, geolist, sourcelist, usagelist, identruleslist)
  
  print(json.dumps(froblist, indent=4))
  foundclass = froblist[0][1] == 0
  classdata = classificationdbo.query.get_or_404(froblist[0][0])
  retdict = { "found" : str(foundclass),
              "classid": classdata.classification_id,
              "recipeid": classdata.recipe_id,
              "label": classdata.label,
              "identlist" : [ str(x[0]) + "|" +str(x[1]) for x in identruleslist ]
            }

    
  return jsonify(retdict)


@classification.route('/classification/add', methods=['GET', 'POST'])
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
  identruleslist = submitobj["ident_list"]
  identrulesscorelist = [ int(i.split("|")[1]) for i in identruleslist ]
  identrulesscorelist.sort()

  classid = submitobj["near_class_id"]
  classrow = classificationdbo.query.get_or_404(classid)


  newclass = classificationdbo(
                                domain_list=domainscorelist,
                                source_list=sourcescorelist,
                                geography_list=geoscorelist,
                                usage_list=usagescorelist,
                                identifiability_rule_list=identrulesscorelist,
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