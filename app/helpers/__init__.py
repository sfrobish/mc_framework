from flask import abort
from flask_login import current_user

def confirm_user_is_admin():
  # prevent non-admins from accessing the page
  if not current_user.user_is_admin:
    abort(403)

def get_nested_children(models, parent_id = None, depth = 1):
 nested_tree_list = []

 for model in models:
     if model.parent_geo_id == parent_id:
         setattr(model, "depth", depth)
         setattr(model, "children", [])

         nested_tree_list.append(model)

         children = get_nested_children(models, model.geo_id, depth + 1)

         if len(children):
             nested_tree_list[-1].children = [o.geo_id for o in children]
             nested_tree_list.extend(children)

 return nested_tree_list
