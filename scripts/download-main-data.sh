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

if [ -f "${MADE_PATH}/data/dblpv13.json" ]; then
    echo "${GREEN} Dataset's already downloaded ${NC}"
    exit 0
fi

if ! [ -f "${MADE_PATH}/data/dblp.v13.7z" ]; then
    echo "${GREEN} Downloading archive to ${MADE_PATH}/data/dblp.v13.7z... ${NC}"
    pip install gdown
    gdown "https://drive.google.com/file/d/1ge2cQ1HTriGE-LjNe5LqEvlpCMAMJNAa/view?usp=sharing" -O ${MADE_PATH}/data/dblp.v13.7z
    # wget https://originalstatic.aminer.cn/misc/dblp.v13.7z --output-file=${MADE_PATH}/data/dblp.v13.7z
fi

echo "${GREEN} Unzip archive... ${NC}"

REQUIRED_PKG="p7zip-full"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "${GREEN} No $REQUIRED_PKG. Setting up $REQUIRED_PKG. ${NC}"
  sudo apt-get --yes install $REQUIRED_PKG
fi

7z x ${MADE_PATH}/data/dblp.v13.7z -o${MADE_PATH}/data/

echo "${GREEN} Final fixing dataset... ${NC}"
sed -i -E "s/NumberInt\(([0-9]+)\)/\1/" ${MADE_PATH}/data/dblpv13.json

echo "${GREEN} End. ${NC}"
