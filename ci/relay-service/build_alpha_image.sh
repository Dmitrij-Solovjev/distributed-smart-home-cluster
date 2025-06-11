#!/bin/sh
set -e

. ci/relay-service/VERSION

PATCH=$(expr "$PATCH" + 1)
PREVIEW_TAG="${MAJOR}.${MINOR}.${PATCH}-alpha"

echo "Building alpha image with tag: $PREVIEW_TAG"

IMAGE="$CI_REGISTRY/$CI_PROJECT_PATH/relay-service:$PREVIEW_TAG"

docker buildx build \
  --platform linux/amd64 \
  -t "$IMAGE" \
  --push relay-service

echo "$PREVIEW_TAG" > ci/relay-service/LAST_BUILD_VERSION
