#!/bin/bash

repo='{{ cookiecutter.project_name }}'
gh_org='{{ cookiecutter.gh_org_name }}'

read -p "Do you want to set git repo remote to git@github.com:$gh_org/$repo.git? (y/n)" choice
case "$choice" in
    y|Y ) echo "Continuing..."; git remote set-url origin git@github.com:$gh_org/$repo.git;
    echo "To undo this please run 'git remote set-url origin git@github.com:Fusion-Power-Plant-Framework/bluemira-template-project.git'";;
    n|N ) echo "Exiting"; exit 0;;
    * ) echo "Invalid input. Exiting"; exit 1;;
esac
