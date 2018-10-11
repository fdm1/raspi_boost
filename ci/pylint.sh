#! /bin/bash

set -eu -o pipefail

cd $(dirname $0)/..
BASE_DIR=$(pwd)

LIBS=(raspi_boost2)
FAILURE=0

for LIB in ${LIBS[@]}; do
  echo "Linting $LIB"

  if ! pylint --rcfile=$BASE_DIR/pylintrc $(find $LIB -name '*.py') $@; then
    FAILURE=1
  fi
done

exit $FAILURE
