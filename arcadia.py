import requests
import ArcadiaAPI as Arc
import Visual
import utility as util
import shell_execution as ssh

class UserSpecs():
	def __init__(self):
		self.export = True
		self.copy = True
		self.impala = True
		self.arcadia = True
		self.modify = True
		self.importVisual = True
	
	def user_defined(self, specs):
		self.export = specs[0]
		self.copy = specs[1]
		self.impala = specs[2]
		self.arcadia = specs[3]
		self.modify = specs[4]
		self.importVisual = specs[5]


def userInput():

	specs = UserSpecs()
	step_num = 6

	print("******************* Arcadia Deployment Automation ***********************")
	print("*                                                                       *")
	print("* Step 1: Export the dashboard from source                              *")
	print("* Step 2: Copy the table from source to target                          *")
	print("* Step 3: Invalidate metadata for the table in Impala                   *")
	print("* Step 4: Invalidata metadata for the table in Arcadia                  *")
	print("* Step 5: Modify dashboard json file (title, database, table, dataset)  *")
	print("* Step 6: Import dashboard to prod environment                          *")
	print("*                                                                       *")
	print("*************************************************************************")

	input_str = input("Do you want to execute all the steps? (y/n):")
	if input_str == 'n' or input_str == 'N':
		input_str = input("Enter the number of the steps (Step 1 -> 1) you want to execute (separated by space):")
		steps = input_str.split()

		specs_list = [True] * step_num
		for x in range(1,step_num+1):
			if not (str(x) in steps):
				specs_list[x-1] = False
		specs.user_defined(specs_list)
		print(specs_list)

	elif(not (input_str == 'y' or input_str == 'Y')):
		print("Please enter y/n")
		util.script_exit()
		
	return specs



def DashboardDeploy():
	# load test & prod config
	test_visual = Visual.load_test_config()
	prod_visual = Visual.load_prod_config()

	# deployment
	Arc.export_visual(test_visual)
	Arc.modify_visual(test_visual,prod_visual)
	Arc.import_visual(prod_visual)


if __name__ == '__main__':

	Arc.create_segment()


	# # load test & prod config
	# test_visual = Visual.load_test_config()
	# prod_visual = Visual.load_prod_config()

	# # take user input
	# specs = userInput()

	# # steps
	# if specs.export == True:
	# 	print("*******************Exporting dashboard")
	# 	Arc.export_visual(test_visual)
	

	# if specs.copy or specs.impala or specs.arcadia:
	# 	print("*******************Shell scripting")
	# 	commands,uploadpathlist,remotepathlist,directory = util.prep_shell_process(specs.copy,specs.impala,specs.arcadia)
	# 	ssh.executeShellCMDS(commands,uploadpathlist,remotepathlist,directory)

	# if specs.modify == True:
	# 	print("*******************Modifying dashboard")
	# 	if specs.export == True:
	# 		Arc.modify_visual(test_visual,prod_visual)
	# 	else:
	# 		input_str = input("Enter the path to the dashboard's json file that is going to be modified:")
	# 		if util.checkFile(input_str):
	# 			Arc.modify_visual(test_visual,prod_visual,input_str)
	# 		else:
	# 			print("Path does not exist. Exit")
	# 			util.script_exit()

	# if specs.importVisual == True:
	# 	print("*******************Importing dashboard")
	# 	if specs.export == True or specs.modify == True:
	# 		Arc.import_visual(prod_visual)
	# 	else:
	# 		input_str = input("Enter the path to the dashboard's json file that is going to be imported:")
	# 		if util.checkFile(input_str):
	# 			Arc.import_visual(prod_visual,input_str)
	# 		else:
	# 			print("Path does not exist. Exit")
	# 			util.script_exit()