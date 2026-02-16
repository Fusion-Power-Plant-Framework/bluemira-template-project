#!/bin/bash

repo='{{ cookiecutter.project_name }}'
gh_org='{{ cookiecutter.gh_org_name }}'


check_remote_repo() {
    local remote=$1
    local owner=$2
    local repo=$3

    local actual=$(git remote get-url "$remote" 2>/dev/null)
    local actual_norm="${actual%.git}"
    actual_norm="${actual_norm%/}"

    local ssh="git@github.com:${owner}/${repo}"
    local https="https://github.com/${owner}/${repo}"

    if [ "$actual_norm" = "$ssh" ] || [ "$actual_norm" = "$https" ]; then
        return 0
    else
        return 1
    fi
}




if git rev-parse --is-inside-work-tree >/dev/null 2>&1 &&
   [ "$(git rev-list --count HEAD 2>/dev/null)" -gt 1 ]; then
    if check_remote_repo origin $gh_org $repo; then
        # Remote already set
    else
        echo "INFO the following steps rewrite the git history and point to your new repository"

        read -p "
    Do you want to clean the git repository, point to your remote and have one initial commit? (y/n)" choice
        case "$choice" in
            y|Y ) echo "Continuing...";
                EMAIL=$(git config user.email)
                NAME=$(git config user.name)
                rm -rf .git
                git init -b main
                git remote set-url origin git@github.com:$gh_org/$repo.git
                git config user.email $EMAIL
                git config user.name $NAME
                git add .gitignore  # avoid commiting ignored things
                git commit -m 'Initial commit'
                git add .
                git commit --amend;;
            n|N ) echo "Exiting"; exit 0;;
            * ) echo "Invalid input. Exiting"; exit 0;;
        esac
    fi
elif git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    read -p "
    Do you want to create a commit with the new changes? (y/n)" choice
        case "$choice" in
            y|Y ) echo "Continuing...";
                git add .
                git commit -m 'Setup template';;
            n|N ) echo "Exiting"; exit 0;;
            * ) echo "Invalid input. Exiting"; exit 0;;
        esac

else
    # echo "Not a repo"
fi
