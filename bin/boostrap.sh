#! /bin/bash

ROOT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../
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


export WORKON_HOME=$HOME/coding/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=$(which python3)
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv raspi_boost
workon raspi_boost
pip install -r requirements.txt