# template-project

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Setting up and using this template

Start by git cloning this repository (or use the "Use this template" button on GitHub).

```bash
git clone git@github.com:Fusion-Power-Plant-Framework/bluemira-template-project.git
cd bluemira-template-project
```

The following strings should set using a "Find and Replace" tool:

| String to place              | Description                                                                               |
|------------------------------|-------------------------------------------------------------------------------------------|
| template-project             | The project name                                                                          |
| template_project             | The main project directory (usally the project name, using underscores instead of dashes) |
| {{ author-name }}            | The name of the author of the project. If there are multiple, add each to the list.       |
| {{ author-email }}           | The email address of the author                                                           |
| {{ copyright-holder }}       | The copyright holder (may be the same as the author(s))                                   |
| {{ copyright-holder-email }} | The copyright holder contact email (may be the same as the author(s))                     |
| {{ org-name }}               | The GitHub organisation. Only applies if using GitHub.                                    |

***All relevant directories should be set/updated too.**

## Setting up Python environment

[Hatch](https://hatch.pypa.io/latest/) is the recommended Python environment manager for this project. However, any Python environment manager can be used.

### With Hatch

To start using Hatch, it must be installed and be accessible from the command line.
See the Hatch [installation](https://hatch.pypa.io/latest/install/) for more information.

A simple way to install Hatch is to run:

```bash
pip install hatch
```

If you can run `hatch -h` then Hatch has been successfully installed.

We recommend setting the `dirs.env` in your hatch config to the following:

```toml
[dirs.env]
virtual = ".hatch"
```

The path to this file can be found by running:

```bash
hatch config find
```

It makes it easier to set the path to environment in your code editor.

Then run:

```bash
hatch shell
```

This will create the default hatch environment in the project folder.

Then set the path to your Python environment in your editor to `.hatch/fusrr/bin/python`

### Without Hatch

Setup and activate your environment with your chosen Python environment manager (pyenv, conda, virtualenv, etc.)

Run the following to install this project as a local editable install, with the necessary optional dependency groups:

```bash
pip install -e '.[dev,test,lint]'
```

## Running reactor designs

## Running tests
