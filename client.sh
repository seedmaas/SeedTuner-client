#!/bin/bash

token=""
extra_requirements=""
server=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -token)
      shift
      token="$1"
      ;;
    -extra_requirements)
      shift
      extra_requirements="$1"
      ;;
    -server)
      shift
      server="$1"
      ;;
    *)
      # Ignore other parameters
      ;;
  esac
  shift
done


echo "token：$token"
echo "ip：$server"


if [ -z "$token" ]; then
    echo "Error: token is empty."
    exit 1
fi

if [ -z "$server" ]; then
    echo "Error: server is empty."
    exit 1
fi

repository_url="git@github.com:seedmaas/SeedTuner-client.git"

git clone --single-branch --branch dev $repository_url 

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

pip install --upgrade pip

cd SeedTuner-client

pip install -r requirements.txt

if [ -n "$extra_requirements" ]; then
    # extra_requirements不为空，执行pip install命令
    pip install -r "$extra_requirements"
fi

git pull

echo "keep listening..."

python3 socketio_client.py --token $token --server $server




