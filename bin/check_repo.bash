#!/bin/bash

REPO="$HOME/wikipedia"
OUT_DIR="$HOME/public_html/control"
INCOMING="${OUT_DIR}/incoming.txt"

mkdir -p ${OUT_DIR}

cd $REPO
git fetch origin
git log HEAD..origin/master --oneline > ${INCOMING}
if [[ -n $(cat ${INCOMING}) ]]; then
  echo "need a new build: incoming"
  #git diff HEAD origin/master
else 
  echo "."
fi
