#! /bin/bash

ROOT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../
VIRTUALENV_DIR=.boost_env
PYBOOST_REPO=https://github.com/JorgePe/pyb00st.git
PYBOOST_DIR=.pyb00st
PYBOOST_LN=pyb00st
# last updated 2017-10-14
GIT_SHA=bf15272481d0541461923820f98983d9f10ebcc9

if [ ! -d $ROOT_DIR/$PYBOOST_DIR ]; then
  git clone $PYBOOST_REPO $PYBOOST_DIR

  pushd $PYBOOST_DIR
  git checkout $GIT_SHA
  popd

  if [ -d $ROOT_DIR/$PYBOOST_LN ]; then
    rm $PYBOOST_LN
  fi

  ln -s $PYBOOST_DIR/pyb00st/ pyb00st
fi


if [ ! -d $ROOT_DIR/$VIRTUALENV_DIR ]; then
  virtualenv $VIRTUALENV_DIR
fi

source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt

cat << EOF

============================================================
boost environment ready. To proceed activate the virtualenv:

  $ source $VIRTUALENV_DIR/bin/activate

============================================================
EOF
