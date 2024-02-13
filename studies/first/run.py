"""Study 1."""

from pathlib import Path

from template_project.reactor import main

build_config_path = Path(Path(__file__).parent, "config/config.json").resolve()
reactor = main(build_config_path)
