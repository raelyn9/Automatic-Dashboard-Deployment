import json
import os
import argparse
import datetime


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())
config = args["conf"]

# json
def convertToJson(data):
    return json.loads(data)

def constructJson(data):
    return json.dumps([data])

def writeToJsonFile(data,name):
    data = json.loads(data)
    with open( name + '.json', 'w') as outfile:
        json.dump(data, outfile)

# file
def checkFile(path):
	if os.path.exists(path):
		return True
	return False

def writeToFile(filename, content):
	with open(filename, 'w+') as f:
		f.write(content)

def load_config():
	conf = json.load(open(config))
	return conf

def clean_up():
	if os.path.exists("visual.json"):
		os.remove("visual.json")
	if os.path.exists("conf.properties"):
			os.remove("conf.properties")

def script_exit():
	clean_up()
	exit()


def create_log_structure(conf):
	timestamp = datetime.datetime.now()
	currentday = timestamp.strftime('%Y%m%d')

	# create folder structure
	if not os.path.exists("logs/"+currentday):
		os.makedirs("logs/"+currentday)
	directory = "logs/"+currentday
	# create log file
	currenttime = timestamp.strftime('%Y%m%d%H%M%S')
	logfile_name="logs/"+currentday+"/arcadia_setup_"+currenttime+".log"
	invalidation="logs/"+currentday+"/invalidation_"+conf['PROD']['DATABASE']+"_"+conf['PROD']['TABLE']+"_"+currenttime+".sql"
	copy="logs/"+currentday+"/copy_"+conf['PROD']['DATABASE']+"_"+conf['PROD']['TABLE']+"_"+currenttime+".sql"

	return logfile_name,invalidation,copy,directory



def prep_shell_process(copy,impala,arcadia):
	commands = []
	uploadpathlist = []
	remotepathlist = []
	conf = load_config()
	logfile_name,invalidation,copy_file,directory = create_log_structure(conf)
	
	if copy:
		copy_query = "CREATE TABLE "+conf['PROD']['DATABASE']+"."+conf['PROD']['TABLE']+" AS SELECT * FROM "+conf['TEST']['DATABASE']+"."+conf['TEST']['TABLE']+";"
		writeToFile(copy_file,copy_query)

		beeline_hive_jdbc_url="hive.9qcrzmt4zwc4rkbp.cazena.internal"
		beeline_hive_jdbc_port_nm="10000"
		beeline_principal="hive/ip-10-2-1-5.cazena.internal@CAZENA.INTERNAL"

		copy_cmd = "beeline -u \"jdbc:hive2://"+beeline_hive_jdbc_url+":"+beeline_hive_jdbc_port_nm+"/"+conf['PROD']['DATABASE']+";AuthMech=1;principal="+beeline_principal+"\" -f "+copy_file
		
		commands.append(copy_cmd)
		uploadpathlist.append(copy_file)
		remotepathlist.append(copy_file)
		writeToFile(logfile_name,copy_cmd)

	if impala or arcadia:
		invalidate_query="invalidate metadata "+conf['PROD']['DATABASE']+"."+conf['PROD']['TABLE']+";"
		writeToFile(invalidation,invalidate_query)
		uploadpathlist.append(invalidation)
		remotepathlist.append(invalidation)

	if impala:
		impala_cmd = conf['SHELL']['IMPALA_SHELL_CMD']+" -f "+invalidation
		commands.append(impala_cmd)
		writeToFile(logfile_name,impala_cmd)

	if arcadia:
		arcadia_cmd = conf['SHELL']['ARCADIA_SHELL_CMD']+" -f "+invalidation
		commands.append(arcadia_cmd)
		writeToFile(logfile_name,arcadia_cmd)

	print("commands",commands)
	print("file path",uploadpathlist)

	return commands,uploadpathlist,remotepathlist,directory
	
