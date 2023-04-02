#!/bin/bash

while [ $# -gt 0 ] ; do
  case $1 in
    -t | --target) W="$2" ;;
  esac
  shift
done

case $W in
    worker) celery -A tasks.app worker --loglevel=INFO;;
    flower) celery -A tasks.app flower --port=5555;;
    fastapi) python main.py
esac