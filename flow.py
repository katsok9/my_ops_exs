#!/usr/bin/python3

import requests
import tarfile
import os
import subprocess
import sys
import time

# get images file

url = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
repo_url = 'https://github.com/bigpandaio/ops-exercise'
health_url = 'http://localhost:3000/health'
filename = url[url.rfind("/")+1:]
reponame = repo_url[repo_url.rfind("/")+1:]
dirname = f"/{reponame}/public/images"
cwd = os.getcwd()
dir_path = f"{cwd}{dirname}"
repo_path = f"{cwd}/{reponame}"

#clone git repo

if not os.path.exists(repo_path):
    ret_code = subprocess.call(f"git clone '{repo_url}' ", shell=True)
    if not ret_code == 0:
        print(f"Error cloning repo, check git config, or url: {repo_url}")
        sys.exit(1)
else:
    print(f"repo: {reponame} already cloned!")

print(f"file name found: {filename}\nDownloading")

r = requests.get(url)
with open("pandapics.tar.gz", "wb") as code:
         code.write(r.content)
code.close()
print(f"Extracting {filename} to {dir_path}")
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
print(f"status: {cmd_status}\noutput: '{cmd_output}'")
if not cmd_status == 0:
    sys.exit(1)

time.sleep(10)

health_res = requests.get(health_url)
if not health_res.status_code == 200:
    print(f"Build not healthy, status_code: {health_res.status_code} ")
    sys.exit(1)
else:
    print(f"Healthcheck return ok: {health_res.status_code}")
