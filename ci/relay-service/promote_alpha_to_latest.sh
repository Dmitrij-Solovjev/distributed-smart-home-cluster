#!/bin/sh
set -e

# Читаем текущую версию из файла
. ci/relay-service/VERSION

BASE="$CI_REGISTRY/$CI_PROJECT_PATH/relay-service"
ALPHA_TAG=$(cat ci/relay-service/LAST_BUILD_VERSION)

# Формируем stable тег (удаляем суффикс -alpha)
STABLE_TAG=$(echo "$ALPHA_TAG" | sed -E 's/-alpha$//')

echo "Promoting alpha $ALPHA_TAG to stable $STABLE_TAG and latest"

docker pull "$BASE:$ALPHA_TAG"

docker tag "$BASE:$ALPHA_TAG" "$BASE:$STABLE_TAG"
docker tag "$BASE:$ALPHA_TAG" "$BASE:latest"

docker push "$BASE:$STABLE_TAG"
docker push "$BASE:latest"

# После успешного релиза — увеличиваем PATCH в VERSION, чтобы новая альфа была уже с большим номером патча
#PATCH=$((PATCH + 1))

#echo "Updating VERSION file to next patch $PATCH"
#echo "MAJOR=$MAJOR" > ci/relay-service/VERSION
#echo "MINOR=$MINOR" >> ci/relay-service/VERSION
#echo "PATCH=$PATCH" >> ci/relay-service/VERSION

# Удаляем LAST_BUILD_VERSION, чтобы не засорять ветку
rm -f ci/relay-service/LAST_BUILD_VERSION

