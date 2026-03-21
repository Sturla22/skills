#!/usr/bin/env bash
set -euo pipefail

if ! python3 -c 'import pytest' >/dev/null 2>&1; then
  python3 -m pip install --upgrade pip
  python3 -m pip install pytest
fi

if command -v arm-none-eabi-gcc >/dev/null 2>&1 \
  && command -v arm-none-eabi-objcopy >/dev/null 2>&1 \
  && command -v arm-none-eabi-size >/dev/null 2>&1; then
  exit 0
fi

sudo apt-get update
sudo apt-get install -y \
  binutils-arm-none-eabi \
  gcc-arm-none-eabi \
  libnewlib-arm-none-eabi \
  libstdc++-arm-none-eabi-newlib
