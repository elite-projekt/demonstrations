#!/bin/bash
#
# Creates folders and files for a new demo.
# Note: must be run in bash. Not PowerShell!

# Enable bash strict mode for error handling
set -euo functrace
failure() {
  local lineno=$1
  local msg=$2
  echo "=============================================="
  echo "Failed at $lineno: $msg"
  echo "=============================================="
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR


# Script Header for prettyness
# Src: http://patorjk.com/software/taag/#p=display&h=1&v=0&c=echo&f=Mini&t=New%20Demo%20Script
echo "                  _                   __                ";
echo " |\ |  _         | \  _  ._ _   _    (_   _ ._ o ._ _|_ ";
echo " | \| (/_ \/\/   |_/ (/_ | | | (_)   __) (_ |  | |_) |_ ";
echo "                                                 |      ";


# Read user input
read -rp 'Enter the name of the demo you would like to create: ' DEMO_ID

if [ -z "${DEMO_ID}" ]
then 
    echo 'Inputs cannot be blank please try again!' 
    exit 100 
fi 

if  [[ "${DEMO_ID}" =~ [^[:lower:]] ]]; then
    echo "Inputs must be lowercase only (a-z, without digits and special chars)" 
    exit 100 
fi

# Set variables
export DEMO_ID
export DEMO_DIR='demos/'${DEMO_ID}'/'
export STACKS_DIR='native/stacks/'${DEMO_ID}'/'
export ORCHESTRATION_CONTROLLER_PATH="./native/src/controller/orchestration_controller.py"


# Check if demo exists
if test -d "$DEMO_DIR"; then
    echo "ERROR: A demo with the name '${DEMO_ID}' already exists!"
    exit 125
fi


# Create files and directories based on the template files in templates
echo "preparing demo directory..."
mkdir "${DEMO_DIR}"
touch "${DEMO_DIR}Dockerfile"
dos2unix "${DEMO_DIR}Dockerfile"

echo "creating endpoints for native app..."
envsubst '${DEMO_ID}' < templates/orchestration-controller.template >> "${ORCHESTRATION_CONTROLLER_PATH}"
dos2unix "${ORCHESTRATION_CONTROLLER_PATH}"


echo "preparing stack directories..."
export DEMO_MODE=secure
mkdir -p "${STACKS_DIR}secure"
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < templates/stackfile.template > "${STACKS_DIR}secure/docker-compose.yml"
dos2unix "${STACKS_DIR}secure/docker-compose.yml"
export DEMO_MODE=unsecure
mkdir -p "${STACKS_DIR}unsecure"
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < templates/stackfile.template > "${STACKS_DIR}unsecure/docker-compose.yml"
dos2unix "${STACKS_DIR}unsecure/docker-compose.yml"

echo "adding demo to gitlab-ci.yml"
source  ./templates/ci-script.template
sed -i '/lint:demo:begin/r'<(echo "$LINTING_SNIPPET") .gitlab-ci.yml
sed -i '/build:demo:begin/r'<(echo "$BUILD_SNIPPET") .gitlab-ci.yml
sed -i '/build:python:begin/r'<(echo "$BUILD_PYTHON_SNIPPET") .gitlab-ci.yml
sed -i '/scan:demo:begin/r'<(echo "$SCAN_SNIPPET") .gitlab-ci.yml
sed -i '/push:demo:begin/r'<(echo "$PUSH_SNIPPED") .gitlab-ci.yml
dos2unix "./.gitlab-ci.yml"


exit 0
