# template-project

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Setting up and using this template

Start by git cloning this repository (or use the "Use this template" button on GitHub).

```bash
git clone git@github.com:Fusion-Power-Plant-Framework/bluemira-template-project.git my_bm_project
cd my_bm_project
```
We use the [cookiecutter](https://github.com/cookiecutter/cookiecutter) project to setup a new bluemira project.

With your local copy of the repository run the following script and fill in the prompts with the details. You will need pip available to install cookiecutter.

```bash
bash scripts/setup_repo.sh
```

Finally to set up your bluemira environment run the following

```bash
bash scripts/install_bluemira.sh -i
```

If you have already have a conda installation you can remove `-i` and the conda step will be skipped.

Any suggested improvements to the setup experience is welcomed, please open an issue or even better a PR!

## Running reactor designs

The example study can be run as shown once the setup has been completed:

```
python studies/first/run.py
```

## Running tests

A test directory is setup (currently empty) once test have been created they can be run with `pytest`.
Once set up this repo creates a github action to run the tests against the current bluemira develop branch which runs on a cron job schedule. By default this runs twice a day.
