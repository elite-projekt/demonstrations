#!/bin/bash

# Fail on errors.
set -e

# Allow the workdir to be set using an env var.
# Useful for CI pipiles which use docker for their build steps
# and don't allow that much flexibility to mount volumes
WORKDIR=/builds/$1/demonstrations/native/native/

cd $WORKDIR

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi # [ -f requirements.txt ]

echo "$@"

if [[ "$@" == "" ]]; then
    pyinstaller --clean -y --dist ./dist/windows --workpath /tmp *.spec 
    chown -R --reference=. ./dist/windows
else
    sh -c "$@"
fi # [[ "$@" == "" ]]
