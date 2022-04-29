#!/bin/bash
#
# Creates folders and files for a new demo.
# Must be run in bash. Not PowerShell!
# Linting: shellcheck

# ref: http://patorjk.com/software/taag/#p=display&h=1&v=0&c=echo&f=Mini&t=New%20Demo%20Script
echo "                  _                   __                ";
echo " |\ |  _         | \  _  ._ _   _    (_   _ ._ o ._ _|_ ";
echo " | \| (/_ \/\/   |_/ (/_ | | | (_)   __) (_ |  | |_) |_ ";
echo "                                                 |      ";


# use array to safe functions of stages for rollback on errors
safe_rollback=( )
add_rollback()
{
    safe_rollback[${#safe_rollback[*]}]=$1;
}

# Enable bash strict mode for error handling
set -euo functrace
failure() {
  local lineno=$1
  local msg=$2
  echo "=============================================="
  echo "Failed at Line $lineno: $msg"
  echo "Performing rollback"
  echo "=============================================="
  while [ ${#safe_rollback[@]} -ge 1 ]; do
    ${safe_rollback[${#safe_rollback[@]}-1]} rollback;
    unset 'safe_rollback[${#safe_rollback[@]}-1]';
  done
  cleanup
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR


while getopts n:t flag
do
    case "${flag}" in
        n) DEMO_ID=${OPTARG};;
        t) DEMO_ID="test";;
        *) echo "usage: init_new_demo.sh [-n <DEMO_NAME>]" && exit;;
    esac
done
# Read user input
if [ -z "${DEMO_ID}" ]; then
    read -rp 'Enter the name of the demo you would like to create: ' DEMO_ID
    if [ -z "${DEMO_ID}" ]
    then 
        echo "Inputs cannot be blank please try again!"
        exit 100 
    fi
    if  [[ "${DEMO_ID}" =~ [^[:lower:]] ]]; then
        echo "Inputs must be lowercase only (a-z, without digits and special chars)" 
        exit 100 
    fi
fi
# set working dir to where THIS init script is so it can be run from anywhere
WORKING_DIR=$(dirname "$(readlink -f "$0")") # path where this init script is
pushd "${WORKING_DIR}"

# Set variables
TEMP_DIR=$(mktemp -d)
export TEMP_DIR
export DEMO_ID
export DEMO_DIR="demos/${DEMO_ID}/"
export DEMO_SRC_DIR="${DEMO_DIR}/src/"
export DEMO_NATIVE_DIR="${DEMO_DIR}/native/"
export DEMO_NATIVE_STACKS_DIR="${DEMO_NATIVE_DIR}/stacks/"
export NATIVEAPP_PATH="native/nativeapp/app.py"

cleanup()
{
  rm -rf -- "${TEMP_DIR}"
}


# Check if demo exists
if test -d "$DEMO_DIR"; then
    echo "ERROR: A demo with the name '${DEMO_ID}' already exists!"
    exit 125
fi

# Create files and directories based on the template files in templates and
# convert the new directories to python packages
rollback_demo_dir()
{
    rm -rf "${DEMO_DIR}"
}
echo "preparing demo directory..."
mkdir -p "${DEMO_DIR}"
add_rollback rollback_demo_dir
mkdir -p "${DEMO_SRC_DIR}"
mkdir -p "${DEMO_NATIVE_DIR}"


touch "${DEMO_DIR}/Dockerfile"
dos2unix "${DEMO_DIR}/Dockerfile"

touch "${DEMO_DIR}/__init__.py"
dos2unix "${DEMO_DIR}/__init__.py"

touch "${DEMO_NATIVE_DIR}/__init__.py"
dos2unix "${DEMO_NATIVE_DIR}/__init__.py"


echo "creating endpoints for native app..."
# shellcheck disable=SC2016
envsubst '${DEMO_ID}' < templates/orchestration-controller.template >> "${DEMO_NATIVE_DIR}/${DEMO_ID}_controller.py"
dos2unix "${DEMO_NATIVE_DIR}/${DEMO_ID}_controller.py"

echo "preparing stack directories..."
export DEMO_MODE=secure
mkdir -p "${DEMO_NATIVE_STACKS_DIR}/secure"
# shellcheck disable=SC2016
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < templates/stackfile.template > "${DEMO_NATIVE_STACKS_DIR}/secure/docker-compose.yml"
dos2unix "${DEMO_NATIVE_STACKS_DIR}/secure/docker-compose.yml"
export DEMO_MODE=unsecure
mkdir -p "${DEMO_NATIVE_STACKS_DIR}/unsecure"
# shellcheck disable=SC2016
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < templates/stackfile.template > "${DEMO_NATIVE_STACKS_DIR}/unsecure/docker-compose.yml"
dos2unix "${DEMO_NATIVE_STACKS_DIR}/unsecure/docker-compose.yml"



# Orchestration Controller Blueprint registration
#####################################
rollback_blueprint_steps()
{
    mv "${TEMP_DIR}"/"$(basename ${NATIVEAPP_PATH})".orig ${NATIVEAPP_PATH}
}
echo "adding demo blueprint controller to NativeApp"
# backup file
cp ${NATIVEAPP_PATH} "${TEMP_DIR}"/"$(basename ${NATIVEAPP_PATH})".orig
add_rollback rollback_blueprint_steps
BP_IMPORT_SNIPPET="from demos.${DEMO_ID}.native import ${DEMO_ID}_controller"
BP_REGISTER_SNIPPET="app.register_blueprint(${DEMO_ID}_controller.orchestration)"
sed -i '/import demo controllers/r'<(echo "$BP_IMPORT_SNIPPET") ${NATIVEAPP_PATH}
sed -i '/register demo controllers/r'<(echo "$BP_REGISTER_SNIPPET") ${NATIVEAPP_PATH}


# NativeApp installer
#####################################
INSTALLER_PATH="native/installer/nativeapp_install_helper.ps1"
rollback_installer_steps()
{
    mv "${TEMP_DIR}"/"$(basename ${INSTALLER_PATH})".orig ${INSTALLER_PATH}
}
echo "adding demo to installer"
INSTALLER_SNIPPET="            run-docker \"pull \$Env:REGISTRY_URL/\$Env:GROUP_NAME/demonstrations/\$Env:${DEMO_ID^^}_REPO\""
# backup file
cp ${INSTALLER_PATH} "${TEMP_DIR}"/"$(basename ${INSTALLER_PATH})".orig
add_rollback rollback_installer_steps
sed -i '/pull the latest docker images/r'<(echo "$INSTALLER_SNIPPET") ${INSTALLER_PATH}


# GitLab CI
rollback_ci_settings()
{
    mv "${TEMP_DIR}"/.gitlab-ci.yml.orig .gitlab-ci.yml
}
echo "adding demo to gitlab-ci.yml"
source  ./templates/ci-script.template
# backup file
cp .gitlab-ci.yml "${TEMP_DIR}"/.gitlab-ci.yml.orig
add_rollback rollback_ci_settings
sed -i '/lint:demo:begin/r'<(echo "$LINTING_SNIPPET") .gitlab-ci.yml
sed -i '/build:demo:begin/r'<(echo "$BUILD_SNIPPET") .gitlab-ci.yml
sed -i '/scan:demo:begin/r'<(echo "$SCAN_SNIPPET") .gitlab-ci.yml
sed -i '/push:demo:begin/r'<(echo "$PUSH_SNIPPED") .gitlab-ci.yml
dos2unix "./.gitlab-ci.yml"


### TEST SUITE BEGIN ###
if [ "${DEMO_ID}" == "test" ]
then
# Create python app (Ref: https://docs.docker.com/compose/gettingstarted/)
cat << EOT > ./demos/test/src/app.py
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
EOT

# create requirements.txt
cat << EOT > ./demos/test/requirements.txt
flask
redis
EOT

# fill Dockerfile
cat << EOT > ./demos/test/Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./src/app.py .
CMD ["flask", "run"]
EOT

cat << EOT >> ./demos/test/native/stacks/unsecure/docker-compose.yml
    ports:
      - "8000:5000"
  redis:
    image: "redis:alpine"
EOT

pushd ./demos/test/native/stacks/unsecure/
docker-compose rm -f -s -v
docker-compose up -d --build --force-recreate
popd
sleep 5
content=$(curl -s --connect-timeout 5 --max-time 5 "http://localhost:8000/")
if ! echo "$content" | grep -"Hello World! I have been seen 1 times."
then
    echo "Error"
    exit 100
fi
content=$(curl -s --connect-timeout 5 --max-time 5 "http://localhost:8000/")
if ! echo "$content" | grep -"Hello World! I have been seen 2 times."
then
    echo "Error"
    exit 100
fi
echo "everything worked fine!"
echo "Performing rollback"
  echo "=============================================="
  while [ ${#safe_rollback[@]} -ge 1 ]; do
    ${safe_rollback[${#safe_rollback[@]}-1]} rollback;
    unset 'safe_rollback[${#safe_rollback[@]}-1]';
  done
fi
### TEST SUITE END ###

cleanup

exit 0
