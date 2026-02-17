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

if uv --help >/dev/null 2>&1; then
    comd=uvx
elif pip --help >/dev/null 2>&1; then
    comd=''
    pip install cookiecutter
else
    read -p "pip and uv not found in PATH. Install local copy of uv to continue setup?.
    Do you want to continue with the setup? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Continuing...";;
        n|N ) echo "Setup aborted."; exit 1;;
        * ) echo "Invalid input. Setup aborted."; exit 1;;
    esac
    if curl --help >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 UV_INSTALL_DIR="$root/bin" sh
    else
        wget -qO- https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 UV_INSTALL_DIR="$root/bin" sh
    fi
    comd=$root/bin/uvx
fi

cwd=$(pwd)
cd $root
DIRECTORY_PRE=($(ls -d */))

$comd cookiecutter $root

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
    rm -rf $root/bin
    mv $DIRECTORY_DIFF/* $root
    mv $DIRECTORY_DIFF/.github $root
    mv $root/scripts_base/* $root/scripts/
    rm -rf scripts_base
    rm -rf $DIRECTORY_DIFF
    mv base $DIRECTORY_DIFF
    rm -rf "{{cookiecutter.project_name}}"
    rm cookiecutter.json
    rm -rf $root/hooks

    if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && \
        ! git rev-parse --verify HEAD >/dev/null 2>&1; then

        git add .gitignore  # avoid commiting ignored things
        git commit -m 'Initial commit'
        git add .
        git commit --amend
    fi
    cd $cwd
else
    echo "Error!" 1>&2
    cd $cwd
    exit 1
fi
