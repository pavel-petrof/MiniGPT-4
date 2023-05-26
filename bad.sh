#!/usr/bin/env bash

host='kot'

remote_dir='/data/ebay/notebooks/$USER/minigpt4'

remote_path="$host:$remote_dir"

rsync -avz --progress \
  --include "pkg.zip" \
  --include "libz.zip" \
  --exclude '.git' \
  --exclude "__pycache__" \
  --exclude ".idea" \
  --exclude "*.csv" \
  --exclude "*.zip" \
  --exclude ".ipynb_checkpoints" \
  --exclude "dask-worker-space" \
  --exclude "sandbox_*" \
  --exclude "checkpoint*" \
  --exclude "*.parquet" \
  --include "ai.ipynb" \
  --exclude "*_tests" \
  --exclude "*.ipynb" \
  --exclude "*.xlsx" \
  --exclude "build" \
  --exclude ".mypy_cache" \
  . $remote_path/


