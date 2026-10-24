#!/bin/sh
cd "$(dirname "$0")" || exit 1
for f in test_*.sh; do
  echo "=============== $f"
  sh "./$f"
done
