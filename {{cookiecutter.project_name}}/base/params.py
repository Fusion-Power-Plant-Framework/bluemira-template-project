# SPDX-FileCopyrightText: {{cookiecutter.copyright_yr}}-present {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
#
# SPDX-License-Identifier: MIT
"""Parameters for {{ cookiecutter.project_name }}"""

from dataclasses import dataclass

from bluemira.base.parameter_frame import Parameter, ParameterFrame

@dataclass
class {{ cookiecutter.project_name }}Params(ParameterFrame):
    """{{ cookiecutter.project_name }} Parameters"""

    R_0: Parameter[float]
    A: Parameter[float]
