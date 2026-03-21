#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
starter_dir="${repo_root}/extras/cmake-nrf52840-template"

cd "${starter_dir}"

cmake --preset host-debug --fresh
cmake --build --preset build-host-debug
ctest --preset test-host-debug

cmake --preset nrf52840-debug --fresh
cmake --build --preset build-nrf52840-debug
