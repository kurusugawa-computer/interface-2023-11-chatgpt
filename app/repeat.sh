#! /bin/bash
HOST=192.168.11.12
PORT=8000
for i in $(seq 100); do
  echo -n "$i "
  curl -X POST -F file=@images/table.jpg http://$HOST:$PORT/inference/
  curl http://$HOST:$PORT/queue_info/
  echo
done
