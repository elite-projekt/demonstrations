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
export DEMO_DIR=${DEMO_ID}'_demo'
export STACKS_DIR='native/stacks/'${DEMO_ID}


# Check if demo exists
if test -d "$DEMO_DIR"; then
    echo "ERROR: A demo with the name '${DEMO_ID}' already exists!"
    exit 125
fi


# Create files and directories based on the template files in demo_templates
echo "preparing demo directory..."
mkdir "${DEMO_DIR}"
touch "${DEMO_DIR}/Dockerfile"
dos2unix "${DEMO_DIR}/Dockerfile"

echo "creating endpoints for native app..."
envsubst '${DEMO_ID}' < demo_templates/orchestration-controller.template >> "./native/src/controller/OrchestrationController.py"
dos2unix "./native/src/controller/OrchestrationController.py"


echo "preparing stack directories..."
export DEMO_MODE=secure
mkdir -p "${STACKS_DIR}/secure"
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < demo_templates/stackfile.template > "${STACKS_DIR}/secure/docker-compose.yml"
dos2unix "${STACKS_DIR}/secure/docker-compose.yml"
export DEMO_MODE=unsecure
mkdir -p "${STACKS_DIR}/unsecure"
envsubst '${DEMO_ID},${DEMO_DIR},${DEMO_MODE}' < demo_templates/stackfile.template > "${STACKS_DIR}/unsecure/docker-compose.yml"
dos2unix "${STACKS_DIR}/unsecure/docker-compose.yml"

echo "creating CI script..."
envsubst '${DEMO_ID}' < demo_templates/ci-script.template > "ci/push-${DEMO_ID}-image.sh"
dos2unix "ci/push-${DEMO_ID}-image.sh"

echo "adding CI script to gitlab-ci.yml"
envsubst '${DEMO_ID}' < demo_templates/ci-yaml.template >> "./.gitlab-ci.yml"
dos2unix "./.gitlab-ci.yml"


exit 0
