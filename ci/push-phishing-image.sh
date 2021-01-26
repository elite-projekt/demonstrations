#!/bin/sh

echo "starting ci script"

mkdir -p /kaniko/.docker
echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json

cd portal
image_name="$CI_REGISTRY_IMAGE/phishing:$CI_COMMIT_BRANCH"
echo "pushing to $image_name"

/kaniko/executor --context "$CI_PROJECT_DIR/Phishing Demo/" --dockerfile "$CI_PROJECT_DIR/Phishing Demo/Dockerfile" --destination "$image_name"
