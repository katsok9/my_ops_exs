#!/usr/bin/python3

import time
import requests
import tarfile
import os
import subprocess
import sys
from pprint import pprint


#clone git repo
subprocess.call("git clone 'https://github.com/bigpandaio/ops-exercise' ", shell=True)


# get images file
url = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
health_url = 'http://localhost:3000/health'
filename = url[url.rfind("/")+1:]
dirname = "/ops-exercise/public/images"
cwd = os.getcwd()
dir_path = cwd + dirname

print("file name found: {}\nDownloading".format(filename))

r = requests.get(url)
with open("pandapics.tar.gz", "wb") as code:
         code.write(r.content)
code.close()
print("Extracting {} to {}".format(filename,dir_path))
# extract images into /public/images
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

tar = tarfile.open(filename, "r:gz")
tar.extractall(path=dir_path)
tar.close()

print("building")
ret_code = subprocess.call("docker ps", shell=True, stdout=subprocess.PIPE)
if not ret_code == 0:
    print("Error runnig docker, check service status")
    sys.exit(1)


cmd = "docker-compose up -d"
(cmd_status, cmd_output) = subprocess.getstatusoutput(cmd)
print("status: {}\noutput: '{}'".format(cmd_status, cmd_output))
if not cmd_status == 0:
    sys.exit(1)

time.sleep(1)

subprocess.call("docker-compose ps", shell=True, stdout=subprocess.PIPE)

print("Checking app health")

health_res = requests.get(health_url)

print(health_res.status_code)

if not health_res.status_code == 200:
    pprint(health_res.json())
    sys.exit(1)

