#!/bin/sh

echo "starting ci script"

mkdir -p /kaniko/.docker
echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json

cd portal
image_name="$CI_REGISTRY_IMAGE/password:$CI_COMMIT_BRANCH"
echo "pushing to $image_name"

/kaniko/executor --context "$CI_PROJECT_DIR/password_demo/" --dockerfile "$CI_PROJECT_DIR/password_demo/Dockerfile" --destination "$image_name"
