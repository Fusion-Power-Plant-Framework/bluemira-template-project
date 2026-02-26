# SPDX-FileCopyrightText: {{cookiecutter.copyright_yr}}-present {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
#
# SPDX-License-Identifier: MIT

"""Materials for {{cookiecutter.project_name}}."""

from matproplib.library.fluids import DTPlasma
from matproplib.library.steel import SS316_L

tf_winding_pack = SS316_L()
plasma = DTPlasma()
