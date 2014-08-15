BRANCH=master
OUT_DIR="${HOME}/public_html/job/${BRANCH}/control"
jsub -mem 6g -once -o "${OUT_DIR}/build-out.txt" -e "${OUT_DIR}/build-err.txt" "${HOME}/bin/runbuild.bash"
