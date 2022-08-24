#!/bin/bash -x

KANIKO_CMD=${KANIKO_CMD:-"sudo docker run --rm -v $(pwd):/workspace gcr.io/kaniko-project/executor:debug"}
DOCKER_CMD=${DOCKER_CMD:-"sudo docker"}

function usage() {
    echo "Usage: $0 -c <context dir> -i <image name> -t <tar path> [-d <dockerfile name>] [-k] [-l] [-p [<override prefix>]]" ; exit
}


while getopts kd:i:c:t:lup flag
do
  case "${flag}" in
    k) INSIDE_KANIKO=1
      ;;
    d) DOCKERFILE_NAME=${OPTARG}
      ;;
    i) IMAGE_NAME=${OPTARG}
      ;;
    c) CONTEXT_DIR=${OPTARG}
      ;;
    t) TAR_PATH=${OPTARG}
      ;;
    l) LOAD_IMAGE=1
      ;;
    u) USE_DOCKER=1
      ;;
    p) IMAGE_PREFIX="registry.code.fbi.h-da.de/elite-projekt/demonstrations"
      if [ "${OPTARG}" != "" ]; then
        IMAGE_PREFIX=${OPTARG}
      fi
      ;;
    *) usage
      ;;
  esac
done

if [ -z "$CONTEXT_DIR" ]; then
  echo "Missing context dir"
  usage
fi

if [ -z "$IMAGE_NAME" ]; then
  echo "Missing image name"
  usage
fi

if [ -z "$TAR_PATH" ] && [ -z "$LOAD_IMAGE" ] && [ -z "$USE_DOCKER" ]; then
  echo "Either specify the tar path, load image or docker parameter"
  usage
fi

shift $(($OPTIND - 1))

if [ "${INSIDE_KANIKO}" == "1" ]; then
  KANIKO_CMD="/kaniko/executor"
fi

if [ "${LOAD_IMAGE}" == "1" ] && [ -z "$TAR_PATH" ]; then
  TAR_PATH="$(mktemp -d)/image.tar"
  DEL_TAR=1
fi

DOCKERFILE_NAME=${DOCKERFILE_NAME:-"Dockerfile"}

if [ "${IMAGE_PREFIX}" != "" ]; then
  IMAGE_NAME=${IMAGE_PREFIX}/${IMAGE_NAME}
fi

# Build image
if [ "${USE_DOCKER}" == "1" ]; then
  ${DOCKER_CMD} build -t ${IMAGE_NAME} -f ${CONTEXT_DIR}/${DOCKERFILE_NAME} ${CONTEXT_DIR}
else
  ${KANIKO_CMD} --context "${CONTEXT_DIR}" --dockerfile "${CONTEXT_DIR}/${DOCKERFILE_NAME}" --no-push --destination "${IMAGE_NAME}" --tarPath "${TAR_PATH}" "$@"
fi

if [ "${LOAD_IMAGE}" == "1" ]; then
  ${DOCKER_CMD} load -i "${TAR_PATH}"
  if [ "${DEL_TAR}" == "1" ]; then
    echo rm "${TAR_PATH}"
  fi
fi
