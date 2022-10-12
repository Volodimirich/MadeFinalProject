#!/bin/bash -x

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [[ -z ${MADE_PATH} ]]; then
    echo "${RED} Please set env variable, path to project: MADE_PATH ${NC}"
    exit 1
fi

if ! [[ -d "${MADE_PATH}/data" ]]; then
    echo "${RED} Something wrong, made project should have data/ dir ${NC}"
    exit 1
fi

if [ -f "${MADE_PATH}/data/dblpv13.jsonl" ]; then
    echo "${GREEN} Dataset's already downloaded ${NC}"
    exit 0
fi

if ! [ -f "${MADE_PATH}/data/dblpv13.zip" ]; then
    echo "${GREEN} Downloading archive to ${MADE_PATH}/data/dblp.v13.7z... ${NC}"
    pip install gdown
    gdown "https://drive.google.com/uc?id=1-Go0pdM_rXjwi2OaIj7tJ7ZjifjLSF43&export=download" -O ${MADE_PATH}/data/dblpv13.zip
    # wget https://originalstatic.aminer.cn/misc/dblp.v13.7z --output-file=${MADE_PATH}/data/dblp.v13.7z
fi

echo "${GREEN} Unzip archive... ${NC}"

REQUIRED_PKG="unzip"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "${GREEN} No $REQUIRED_PKG. Setting up $REQUIRED_PKG. ${NC}"
  sudo apt-get --yes install $REQUIRED_PKG
fi

unzip ${MADE_PATH}/data/dblpv13.zip -d ${MADE_PATH}/data/

echo "${GREEN} End. ${NC}"
