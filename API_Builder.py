import requests
import utility as util

# read params from config.json
config = util.load_config()

# general session that can be used for future API calls
session = requests.session()
session.headers['AUTHORIZATION'] = 'apikey %s' % config['APIKey']


# print api result
def print_result(response):
    print("---------returns----------")
    print(response.status_code)
    print(response.text)

# api request caller
def api_resp_check(response):
    if response.status_code != 200:
        print("----------ERROR-------------")
        print_result(response)
        util.script_exit()

# api endpoint constructor
def api_url_ctor(data_type, name=None, id=None):
    if name:
        return '/adminapi/v1/'+data_type.value+'?name='+name
    elif id:
        return '/adminapi/v1/'+data_type.value+'/'+id
    return '/adminapi/v1/'+data_type.value

# accept payload json format
def api_payload_format(payload):
    return {'data':util.constructJson(payload)}

# api payload constructor
def api_payload_ctor(data_type, data):

    payload = ''
    if data_type.value == 'visuals':
        payload = {'title':data}
    elif data_type.value == 'datasets':
        payload = {'dataset_id':data}
    elif data_type.value ==  'workspaces':
        payload = {'workspace_id':data}
    
    return api_payload_format(payload)

def arc_api_get_request(endpoint, params=None, data=None):

    if data and params:
        response = session.get(config['API_URL']+endpoint, params=params, data=data)
    elif data:
        response = session.get(config['API_URL']+endpoint, data=data)
    elif params:
        response = session.get(config['API_URL']+endpoint, params=params)
    else:
        response = session.get(config['API_URL']+endpoint)
    api_resp_check(response)
    return response

def arc_api_post_request(endpoint, params=None, data=None, files=None):

    if files:
        response = session.post(config['API_URL']+endpoint, files=files,data=data)  # import
    elif data and params:
        response = session.post(config['API_URL']+endpoint, params=params, data=data)
    elif data:
        response = session.post(config['API_URL']+endpoint, data=data)
    elif params:
        response = session.post(config['API_URL']+endpoint, params=params)
    else:
        response = session.post(config['API_URL']+endpoint)
    api_resp_check(response)
    return response
