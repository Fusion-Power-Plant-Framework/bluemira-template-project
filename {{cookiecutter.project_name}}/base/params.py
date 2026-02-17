{%- set words = cookiecutter.project_name | replace('-', ' ') | replace('_', ' ') | trim | title | replace(' ', '') -%}
{%- set pascal = words[:1] | upper ~ words[1:] -%}
# SPDX-FileCopyrightText: {{cookiecutter.copyright_yr}}-present {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
#
# SPDX-License-Identifier: MIT
"""Parameters for {{ cookiecutter.project_name }}"""

from dataclasses import dataclass

from bluemira.base.parameter_frame import Parameter, ParameterFrame

@dataclass
class {{ pascal }}Params(ParameterFrame):
    """{{ cookiecutter.project_name }} Parameters"""

    R_0: Parameter[float]
    A: Parameter[float]
