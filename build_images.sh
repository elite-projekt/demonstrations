#!/bin/bash

./build_image.sh -c demos/uhh_ducky_mitm/container/mitmproxy -i uhh_ducky_mitm_proxy -u -p
./build_image.sh -c demos/uhh_ducky_mitm/container/nginx -i uhh_ducky_mitm_web -u -p
./build_image.sh -c demos/uhh_ducky_mitm/container/nginx -d Dockerfile_en -i uhh_ducky_mitm_web_en -u -p
