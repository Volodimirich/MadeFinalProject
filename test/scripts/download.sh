#!/bin/bash
if [ -d "../../dataset" ] && [ -f "../../dataset/dblpv13.json" ]
then
    exit 0
else
    if ! [ -d "./dblp.v13.7z" ]
    then
        mkdir "../../dataset"
    fi

    if ! [ -f "./dblp.v13.7z" ]
    then
        wget https://originalstatic.aminer.cn/misc/dblp.v13.7z
    fi
fi

apt-get update
apt-get install apt-get install p7zip-full
7z x dblp.v13.7z -o../../dataset/
rm dblp.v13.7z
sed -i -E "s/NumberInt\(([0-9]+)\)/\1/" ../../dataset/dblpv13.json
