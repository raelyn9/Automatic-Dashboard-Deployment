import paramiko
import os,sys,time 
import socket
import utility as util

conf = util.load_config()
 
class Ssh_Util:
    "Class to connect to remote server" 
 
    def __init__(self,commands):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host= conf['SSH']['HOST']
        self.port = conf['SSH']['PORT']
        self.username = conf['SSH']['USERNAME']
        self.password = conf['SSH']['PASSWORD']
        self.timeout = float(conf['SSH']['TIMEOUT'])
        self.commands = commands
        self.uploadremotefilepath = "/home/fvdl_project_rbu/query"

 
    def connect(self):
        "Login to the remote server"
        try:
            #Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print ("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            #Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #Connect to the server

            self.client.connect(hostname=self.host, port=self.port,username=self.username,password=self.password,timeout=self.timeout, allow_agent=False, look_for_keys=False)    
            print ("Connected to the server",self.host)
        except paramiko.AuthenticationException:
            print ("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print ("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print ("Connection timed out")
            result_flag = False
        except Exception as e:
            print ('\nException in connecting to the server')
            print ('PYTHON SAYS:',e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True
 
        return result_flag    
 
    def execute_command(self,commands):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command."""
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                for command in commands:
                    print ("Executing command --&gt; {}".format(command))
                    stdin, stdout, stderr = self.client.exec_command(command,timeout=10)    
                    for line in stdout.readlines():
                        print (line) 
                    for line in stderr.readlines():
                        print (line)    
                self.client.close()
            else:
                print ("Could not establish SSH connection")
                result_flag = False   
        except socket.timeout as e:
            print ("Command timed out.", command)
            self.client.close()
            result_flag = False                
        except paramiko.SSHException:
            print ("Failed to execute the command!",command)
            self.client.close()
            result_flag = False    
 
        return result_flag

    def upload_file(self,uploadlocalfilepathlist,remotepathlist,directory):
        "This method uploads the file to remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client= self.client.open_sftp()
                for  uploadlocalfilepath,remotefilepath in zip(uploadlocalfilepathlist,remotepathlist):
                    print("path test ",uploadlocalfilepath,remotefilepath)
                    ftp_client.put(uploadlocalfilepath,remotefilepath)
                ftp_client.close() 
                self.client.close()
            else:
                print ("Could not establish SSH connection")
                result_flag = False  
        except Exception as e:
            print ('\nUnable to upload the file to the remote server',remotefilepath)
            print ('PYTHON SAYS:',e)
            result_flag = False
            ftp_client.close()
            self.client.close()

        return result_flag

 
def executeShellCMDS(commands,uploadpathlist,remotepathlist,directory):
    #Initialize the ssh object
    ssh_obj = Ssh_Util(commands)

    # create log directory if not exists
    command = []
    content = 'mkdir -p ' + directory
    command.append(content)
    if ssh_obj.execute_command(command) is True:
        print ("Commands executed\n")
    else:
        print ("Unable to execute the commands")

    # upload query files
    if ssh_obj.upload_file(uploadpathlist,remotepathlist,directory) is True:
        print ("File uploaded successfully")
    else:
        print  ("Failed to upload the file")

    # execute commands
    if ssh_obj.execute_command(ssh_obj.commands) is True:
        print ("Commands executed\n")
    else:
        print ("Unable to execute the commands")