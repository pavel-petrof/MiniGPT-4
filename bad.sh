#!/usr/bin/env bash

host='kot'

remote_dir='/data/ebay/notebooks/$USER/minigpt4'

remote_path="$host:$remote_dir"

rsync -avz --progress \
  --exclude '.git' \
  --exclude "__pycache__" \
  --exclude ".idea" \
  --exclude "*.csv" \
  --exclude "*.zip" \
  --exclude ".ipynb_checkpoints" \
  --exclude "sandbox_*" \
  --exclude "checkpoint*" \
  --exclude "*.parquet" \
  --exclude "*_tests" \
  --exclude "*.ipynb" \
  --exclude "*.xlsx" \
  --exclude "build" \
  --exclude ".mypy_cache" \
  . $remote_path/

rsync -avz \
  --include='*/' \
  --exclude='*-checkpoint.ipynb' \
  --include='*.ipynb' \
  --exclude='*' \
  $remote_path ..


