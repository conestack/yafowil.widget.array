#!/bin/sh

set -e

./bin/coverage run \
    --source src/yafowil/widget/array \
    --omit src/yafowil/widget/array/example.py \
    -m yafowil.widget.array.tests
./bin/coverage report
./bin/coverage html
