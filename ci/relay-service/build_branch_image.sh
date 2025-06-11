#!/bin/sh
set -e

. ci/relay-service/VERSION

# Берём короткий хеш ветки (название ветки или коммит - что точнее, зависит от CI)
# CI_COMMIT_REF_SLUG — slug версии ветки, обычно норм
BRANCH_HASH=$(echo "$CI_COMMIT_SHA" | cut -c1-7)

TIMESTAMP=$(date +%Y%m%d.%H%M%S)
PREVIEW_TAG="${MAJOR}.${MINOR}.${PATCH}-${BRANCH_HASH}-preview.${TIMESTAMP}"

echo "Building preview image with tag: $PREVIEW_TAG"

IMAGE="$CI_REGISTRY/$CI_PROJECT_PATH/relay-service:$PREVIEW_TAG"

docker buildx build \
  --platform linux/amd64 \
  -t "$IMAGE" \
  --push relay-service

echo "$PREVIEW_TAG" > ci/relay-service/LAST_BUILD_VERSION
