#!/bin/bash

set -eo pipefail

echo "Bluemira Project Setup"

script_dir=$(dirname "$0")

root=$script_dir"/../"

if [ ! -d $root/'{{cookiecutter.project_name}}' ]; then
  echo "Project has already been setup."
  echo "If you would like to re-setup the project you can run 'git clean -idX .'"
  echo "to reset the repo to a clean state."
  exit 0
fi

pip install -q cookiecutter

cwd=$(pwd)
cd $root

DIRECTORY_PRE=($(ls -d */))

cookiecutter $root

DIRECTORY_POST=($(ls -d */))

DIRECTORY_DIFF=()
for i in "${DIRECTORY_POST[@]}"; do
    skip=
    for j in "${DIRECTORY_PRE[@]}"; do
        [[ $i == $j ]] && { skip=1; break; }
    done
    [[ -n $skip ]] || DIRECTORY_DIFF+=("$i")
done

if [ ${#DIRECTORY_DIFF[@]} -eq 1 ]; then
    mv $DIRECTORY_DIFF/* $root
    mv $DIRECTORY_DIFF/.github $root
    rm -rf $DIRECTORY_DIFF
    mv base $DIRECTORY_DIFF
    rm -rf "{{cookiecutter.project_name}}"
    rm cookiecutter.json
    cd $cwd
else
    echo "Error!" 1>&2
    cd $cwd
    exit 1
fi
