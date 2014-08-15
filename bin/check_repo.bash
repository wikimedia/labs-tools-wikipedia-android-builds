#!/bin/bash

REPO="$HOME/wikipedia"
BRANCH=master
OUT_DIR="$HOME/job/${BRANCH}/control"
INCOMING="${OUT_DIR}/incoming.txt"

mkdir -p ${OUT_DIR}

cd $REPO
git fetch origin
git log HEAD..origin/master --oneline > ${INCOMING}
if [[ -n $(cat ${INCOMING}) ]]; then
  echo "need a new build"
  #git diff HEAD origin/master
  jsub -mem 6g -once -o "${OUT_DIR}/build-out.txt" -e "${OUT_DIR}/build-err.txt" "${HOME}/bin/runbuild.bash"
else 
  echo "no updates"
fi
