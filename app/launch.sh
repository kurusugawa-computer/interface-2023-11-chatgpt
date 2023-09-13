#!/bin/bash
cd "$(dirname "$0")" || exit 1
xhost +local:root
sudo docker run --rm -it \
  --network host \
  --gpus all \
  --env "DISPLAY=$DISPLAY" \
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  -v "$PWD:/workspace" \
  -w /workspace \
  nkats/interface_od_server_by_chatgpt bash -c "/setup.sh && bash ./download_models.sh && bash"
