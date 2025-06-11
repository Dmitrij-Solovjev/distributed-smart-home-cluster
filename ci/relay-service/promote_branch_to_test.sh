#!/bin/sh
set -e

. ci/relay-service/VERSION

BRANCH_HASH=$(echo "$CI_COMMIT_SHA" | cut -c1-7)

BASE="$CI_REGISTRY/$CI_PROJECT_PATH/relay-service"
PREVIEW_TAG=$(cat ci/relay-service/LAST_BUILD_VERSION)

TEST_TAG="${MAJOR}.${MINOR}.${PATCH}-${BRANCH_HASH}"

echo "Building test image with tag: $TEST_TAG from preview $PREVIEW_TAG"

docker pull "$BASE:$PREVIEW_TAG"
docker tag "$BASE:$PREVIEW_TAG" "$BASE:$TEST_TAG"
docker push "$BASE:$TEST_TAG"
