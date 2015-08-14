#!/usr/bin/env bash
set -euo pipefail

declare latest_path='/srv/builds/public_html/runs/latest'

[[ -d "$latest_path" ]] || mkdir "$latest_path"

(cd "$latest_path";
  curl -O 'https://integration.wikimedia.org/ci/job/apps-android-wikipedia-publish/lastSuccessfulBuild/artifact/{app/build/outputs/apk/app-alpha-release.apk,meta.json}'
  mv app-alpha-release.apk wikipedia.apk
)