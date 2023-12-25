#!/bin/bash

token=""
seedtuner_client_path=""
extra_requirements=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -token)
      shift
      token="$1"
      ;;
    -seedtuner_client_path)
      shift
      seedtuner_client_path="$1"
      ;;
    -extra_requirements)
      shift
      extra_requirements="$1"
      ;;
    *)
      # Ignore other parameters
      ;;
  esac
  shift
done

echo "token：$token"
echo "用户端路径：$seedtuner_client_path"
echo "额外依赖路径：$extra_requirements"


if [ -z "$token" ]; then
    echo "Error: token is empty."
    exit 1
fi

if [ -z "$seedtuner_client_path" ]; then
    echo "Error: seedtuner_client_path is empty."
    exit 1
fi

# Print parameters



repository_url="git@github.com:seedmaas/SeedTuner-client.git"

git clone --single-branch --branch dev $repository_url $seedtuner_client_path

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

pip install --upgrade pip

cd $seedtuner_client_path

pip install -r requirements.txt

if [ -n "$extra_requirements" ]; then
    # extra_requirements不为空，执行pip install命令
    pip install -r "$extra_requirements"
fi

echo "keep listening..."

python3 socketio_client.py $token



