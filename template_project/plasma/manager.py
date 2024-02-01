# SPDX-FileCopyrightText: 2024-present {{ copyright-holder }} <{{ copyright-holder-email }}>
#
# SPDX-License-Identifier: MIT


from bluemira.base.reactor import ComponentManager

# To manage access to properties of the components we need some `ComponentManagers`


class Plasma(ComponentManager):
    """Plasma component manager."""

    def lcfs(self):
        """Get separatrix"""
        return (
            self.component()
            .get_component("xz")
            .get_component("LCFS")
            .shape.boundary[0]
        )
