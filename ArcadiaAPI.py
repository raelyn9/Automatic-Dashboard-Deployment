import requests
from enum import Enum

import API_Builder as API
import utility as util

class DATA(Enum):
    VISUAL = "visuals"
    DATASET = "datasets"
    WORKSPACE = "workspaces"
    SEGMENT = "segments"

# get data item by name
def get_item_by_name(data_type,name):
    api_url = API.api_url_ctor(data_type,name)
    return API.arc_api_get_request(api_url)

# get data item id
def get_item_id(data_type,name):
    resp = util.convertToJson(get_item_by_name(data_type,name).text)
    return resp[0]['id']

# update visual component
def update_visual_component(id,data_type,data):
    api_url = API.api_url_ctor(DATA.VISUAL,'',str(id))
    payload = API.api_payload_ctor(data_type,data)
    response = API.arc_api_post_request(api_url,'',payload)


# update
def update_visual(name,new_name,dataset_name,workspace_name):
    id = get_item_id(DATA.VISUAL,name)
    print ("id",id)

    # update title
    update_visual_component(id,DATA.VISUAL,new_name)

    # update dataset
    dataset_id = get_item_id(DATA.DATASET,dataset_name)
    update_visual_component(id,DATA.DATASET,dataset_id)

    #update workspace
    workspace_id = get_item_id(DATA.WORKSPACE,workspace_name)
    update_visual_component(id,DATA.WORKSPACE,workspace_id)


# export
def export_visual(test_visual):
    api_url = '/migration/api/export/'

    payload = {'dashboards': '['+test_visual.id+']', 'filename': 'apitestmigration', 'dry_run':'False'}
    response = API.arc_api_get_request(api_url,payload)

    with open('visual.json', 'w') as f:
        f.write(response.text)

# import
def import_visual(prod_visual,filename=None):
	api_url = '/migration/api/import/'

	payload = {'dry_run': False, "dataconnection_name":prod_visual.connection}
	files = {}
	if filename:
		files = {'import_file': open(filename,'r')}
	else:
		files = {'import_file': open('new_visual.json','r')}
	response = API.arc_api_post_request(api_url,'',payload,files)

	# clean up
	util.clean_up()


# find & replace
def modify_visual(test_visual,prod_visual,filename=None):
	filename = 'visual.json'
	if filename:
		filename = filename
	with open(filename, 'r+') as myfile:
		data = myfile.read()

		data = data.replace(test_visual.title, prod_visual.title)
		data = data.replace(test_visual.dataset, prod_visual.dataset)
		data = data.replace(test_visual.database, prod_visual.database)
		data = data.replace(test_visual.table, prod_visual.table)

		util.writeToJsonFile(data,'new_visual')


# segment
def create_segment():
    # api_url = '/adminapi/v1/segments'
    # payload = {
    #     "name": "testttt",
    #     "dataset_id": 238,
    #     "data": {
    #     "group": "department seg",
    #     "filters": [
    #         "[Designation] in ('Technical manager')"
    #     ],
    #     "entities": [],
    #     "applyToNewVisuals": False
    #     }
    # }

    # payload = API.api_payload_format(payload)

    api_url = API.api_url_ctor(DATA.SEGMENT)

    seg_name = "testttt"
    dataset_id = 238
    group = "department seg"

    seg_filter = "[Designation] in ('Technical manager')"

    payload = {
        "name": seg_name,
        "dataset_id": dataset_id,
        "data": {
        "group": group,
        "filters": [
            seg_filter
        ],
        "entities": [],
        "applyToNewVisuals": False
        }
    }

    payload = API.api_payload_format(payload)

    response = API.arc_api_post_request(api_url,'',payload)

# roles
def create_role():

    payload = {
      "name": "HAHAHA",
      "desc": "HHHHH",
      "groups": ["data_analyst"],
      "privs": [
          {"ptype": "system",
           "perms": []
          },
          {"ptype": "dataconn",
           "dclist": ["-1"],
           "perms": ["dc_aviews", "dc_upload", "dc_explore"]
          },
          {"ptype": "dataset",
           "dcid": "-1",
           "dslist": ["-1"],
           "perms": ["ds_manage", "ds_appedit", "ds_appview"]
          }
       ]
   }