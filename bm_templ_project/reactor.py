# SPDX-FileCopyrightText: 2024-present <set:author-name> <<set:author-email>>
#
# SPDX-License-Identifier: <set:license>

"""The reactor design example."""

# %%

from bluemira.base.parameter_frame import EmptyFrame
from bluemira.base.reactor import Reactor
from bluemira.base.reactor_config import ReactorConfig

from bm_templ_project.plasma.builder import PlasmaBuilder
from bm_templ_project.plasma.desinger import PlasmaDesigner
from bm_templ_project.plasma.manager import Plasma
from bm_templ_project.tf_coil.builder import TFCoilBuilder
from bm_templ_project.tf_coil.designer import TFCoilDesigner
from bm_templ_project.tf_coil.manager import TFCoil

# %% [markdown]
#
# # Simplistic Reactor Design
#
# This example show hows to set up a simple reactor, consisting of a plasma and
# a single TF coil.
# The TF coil will be optimised such that its length is minimised,
# whilst maintaining a minimum distance to the plasma.
#
# To do this we'll run through how to set up the parameters for the build,
# how to define the `Builder`s and `Designer`s (including the optimisation problem)
# for the plasma and TF coil,
# and how to run the build with configurable parameters.
#


# %%
class MyReactor(Reactor):
    """A simple reactor with two components."""

    plasma: Plasma
    tf_coil: TFCoil


# %% [markdown]
# ## Setup and Run
# Now let us setup our build configuration.
# This could be stored as a JSON file and read in but for simplicity it is all written
# here.
# Notice there are no 'global' parameters as neither of the components share a variable.

# %%
build_config = {
    # This reactor has no global parameters, but this key would usually
    # be used to set parameters that are shared between components
    "params": {},
    "Plasma": {
        "designer": {
            "params": {
                "R_0": {
                    "value": 9.0,
                    "unit": "m",
                    "source": "Input",
                    "long_name": "Major radius",
                },
                "z_0": {
                    "value": 0.0,
                    "unit": "m",
                    "source": "Input",
                    "long_name": "Reference vertical coordinate",
                },
                "A": {
                    "value": 3.1,
                    "unit": "dimensionless",
                    "source": "Input",
                    "long_name": "Aspect ratio",
                },
                "kappa_u": {
                    "value": 1.6,
                    "unit": "dimensionless",
                    "source": "Input",
                    "long_name": "Upper elongation",
                },
                "kappa_l": {
                    "value": 1.8,
                    "unit": "dimensionless",
                    "source": "Input",
                    "long_name": "Lower elongation",
                },
                "delta_u": {
                    "value": 0.4,
                    "unit": "dimensionless",
                    "source": "Input",
                    "long_name": "Upper triangularity",
                },
                "delta_l": {
                    "value": 0.4,
                    "unit": "dimensionless",
                    "source": "Input",
                    "long_name": "Lower triangularity",
                },
                "phi_neg_u": {"value": 0, "unit": "degree", "source": "Input"},
                "phi_pos_u": {"value": 0, "unit": "degree", "source": "Input"},
                "phi_neg_l": {"value": 0, "unit": "degree", "source": "Input"},
                "phi_pos_l": {"value": 0, "unit": "degree", "source": "Input"},
            },
        },
    },
    "TF Coil": {
        "params": {},
        "designer": {
            "runmode": "run",
            "param_class": "PrincetonD",
            "var_dict": {
                "x1": {"value": 3.0, "fixed": True},
                "x2": {"value": 15, "lower_bound": 12},
            },
        },
        "builder": {
            "params": {
                "tf_wp_width": {
                    "value": 0.6,
                    "unit": "m",
                    "source": "Input",
                    "long_name": "Width of TF coil winding pack",
                },
                "tf_wp_depth": {
                    "value": 0.8,
                    "unit": "m",
                    "source": "Input",
                    "long_name": "Depth of TF coil winding pack",
                },
            },
        },
    },
}

# %% [markdown]
#
# Now we set up our ParameterFrames

# %%

reactor_config = ReactorConfig(build_config, EmptyFrame)


# %% [markdown]
#
# We create our plasma

# %%
plasma_designer = PlasmaDesigner(
    reactor_config.params_for("Plasma", "designer"),
    reactor_config.config_for("Plasma", "designer"),
)
plasma_parameterisation = plasma_designer.execute()

plasma_builder = PlasmaBuilder(
    plasma_parameterisation.create_shape(),
    reactor_config.config_for("Plasma"),
)
plasma = Plasma(plasma_builder.build())

# %% [markdown]
#
# We create our TF coil

# %%
tf_coil_designer = TFCoilDesigner(
    plasma.lcfs(),
    None,
    reactor_config.config_for("TF Coil", "designer"),
)
tf_parameterisation = tf_coil_designer.execute()

tf_coil_builder = TFCoilBuilder(
    reactor_config.params_for("TF Coil", "builder"),
    tf_parameterisation.create_shape(),
)
tf_coil = TFCoil(tf_coil_builder.build())

# %% [markdown]
#
# Finally we add the components to the reactor and show the CAD

# %%
reactor = MyReactor("Simple Example", n_sectors=1)

reactor.plasma = plasma
reactor.tf_coil = tf_coil

reactor.show_cad(n_sectors=1)
reactor.show_cad("xz")
