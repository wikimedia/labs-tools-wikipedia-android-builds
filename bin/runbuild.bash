#!/bin/bash

export ANDROID_HOME="$HOME/android-sdk-linux"
export ANDROID_BUILD_TOOLS="$ANDROID_HOME/build-tools/20.0.0"
export M2_HOME="$HOME/apache-maven-3.1.1"
export M2="$M2_HOME/bin"
export PATH=$M2:$ANDROID_HOME/tools:$ANDROID_BUILD_TOOLS:$JAVA_HOME/bin:$PATH

REPO="$HOME/wikipedia"
BRANCH=master
START_TIME=`TZ="UTC" date "+%Y-%m-%dT%H:%M"`
OUT_DIR="$HOME/public_html/job/${BRANCH}"
JOB_DIR="${OUT_DIR}/${START_TIME}"

if [[ -d ${JOB_DIR} ]]; then
  echo "${JOB_DIR} already exists!"
  exit
fi

mkdir -p ${JOB_DIR}
cd ${OUT_DIR}
ln -sf ${START_TIME} latest

cd ${REPO}
git checkout ${BRANCH}
git reset --hard 
git log HEAD..origin/master --oneline > ${JOB_DIR}/commits.txt
git diff HEAD origin/${BRANCH} > ${JOB_DIR}/diffs.txt
git pull origin ${BRANCH}

# just run inside the app folder so we don't try to run the instrumentation tests
cd ${REPO}/wikipedia
mvn clean install > ${JOB_DIR}/mvn.log

# copy more artifacts:
cp target/wikipedia*.apk ${JOB_DIR}/
