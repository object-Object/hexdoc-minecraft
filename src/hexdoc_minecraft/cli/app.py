import logging
from pathlib import Path
from zipfile import ZipFile

from hexdoc.cli.utils.args import PropsOption, VerbosityOption
from hexdoc.core import Properties
from hexdoc.utils import setup_logging
from typer import Typer

from ..piston_meta import VersionManifestV2
from ..properties import MinecraftProps

logger = logging.getLogger(__name__)

CACHE_ROOT = Path(".hexdoc_minecraft")


app = Typer(
    pretty_exceptions_enable=False,
    context_settings={
        "help_option_names": ["--help", "-h"],
    },
)


@app.command()
def fetch(
    *,
    props_file: PropsOption,
    verbosity: VerbosityOption = 1,
    ci: bool = False,
):
    """Download the Minecraft client jar."""
    setup_logging(verbosity, ci)

    props = Properties.load(props_file)
    minecraft_props = MinecraftProps.model_validate(props.extra["minecraft"])

    jar_path = CACHE_ROOT / minecraft_props.version / "client.jar"

    manifest = VersionManifestV2.fetch()
    package = manifest.fetch_package(minecraft_props.version)
    package.downloads.client.fetch_file(jar_path)

    logger.info("Done.")


@app.command()
def unzip(
    *,
    props_file: PropsOption,
    verbosity: VerbosityOption = 1,
    ci: bool = False,
):
    """Partially extract the Minecraft client jar."""
    setup_logging(verbosity, ci)

    props = Properties.load(props_file)
    minecraft_props = MinecraftProps.model_validate(props.extra["minecraft"])

    version_dir = CACHE_ROOT / minecraft_props.version
    jar_path = version_dir / "client.jar"

    with ZipFile(jar_path) as jar:
        for name in jar.namelist():
            if name.startswith(
                (
                    "assets/minecraft/blockstates/",
                    "assets/minecraft/models/",
                    "assets/minecraft/textures/block/",
                    "assets/minecraft/textures/item/",
                )
            ):
                jar.extract(name, version_dir / "resources")

    logger.info("Done.")


if __name__ == "__main__":
    app()
