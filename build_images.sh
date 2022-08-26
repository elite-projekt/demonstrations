#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

function build_demo() {
  DOCKER_PATH=$1
  TAG=$2

  "${SCRIPT_DIR}/build_image.sh" -c ${DOCKER_PATH} -i ${TAG} -u -p
}

build_demo "${SCRIPT_DIR}/demos/uhh_ducky_mitm/container/mitmproxy" uhh_ducky_mitm_proxy
build_demo "${SCRIPT_DIR}/demos/uhh_ducky_mitm/container/nginx" uhh_ducky_mitm_web

build_demo "${SCRIPT_DIR}/demos/fokusrnware" fokusrnware

build_demo "${SCRIPT_DIR}/demos/ransomware" ransomware

build_demo "${SCRIPT_DIR}/demos/phishing" phishing

build_demo "${SCRIPT_DIR}/demos/password" password
