# SPDX-FileCopyrightText: 2024-present {{ copyright-holder }} <{{ copyright-holder-email }}>
#
# SPDX-License-Identifier: MIT

from bluemira.base.reactor import ComponentManager


class TFCoil(ComponentManager):
    """TF Coil component manager."""

    def wp_volume(self):
        """Get winding pack volume"""
        return (
            self.component()
            .get_component("xyz")
            .get_component("Winding pack")
            .shape.volume()
        )
