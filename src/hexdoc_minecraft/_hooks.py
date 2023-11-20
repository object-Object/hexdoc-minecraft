from importlib.resources import Package
from pathlib import Path

from github import Github
from hexdoc.core import ModResourceLoader
from hexdoc.minecraft.assets import HexdocAssetLoader
from hexdoc.plugin import (
    HookReturn,
    ModPlugin,
    ModPluginImpl,
    VersionedModPlugin,
    hookimpl,
)
from typing_extensions import override

from .__gradle_version__ import FULL_VERSION, GRADLE_VERSION
from .__version__ import PY_VERSION
from .asset_loader import MinecraftAssetLoader
from .minecraft_assets import MinecraftAssetsRepo
from .properties import MinecraftProps


class MinecraftPlugin(ModPluginImpl):
    @staticmethod
    @hookimpl
    def hexdoc_mod_plugin(branch: str) -> ModPlugin:
        return MinecraftModPlugin(branch=branch)


class MinecraftModPlugin(VersionedModPlugin):
    @property
    def modid(self) -> str:
        return "minecraft"

    @property
    def full_version(self) -> str:
        return FULL_VERSION

    @property
    def plugin_version(self) -> str:
        return PY_VERSION

    @property
    def mod_version(self) -> str:
        return GRADLE_VERSION

    def resource_dirs(self) -> HookReturn[Package]:
        from hexdoc_minecraft._export import generated, resources

        return [generated, resources]

    @override
    def asset_loader(
        self,
        loader: ModResourceLoader,
        *,
        site_url: str,
        asset_url: str,
        render_dir: Path,
    ) -> HexdocAssetLoader:
        minecraft_props = MinecraftProps.model_validate(loader.props.extra["minecraft"])
        return MinecraftAssetLoader(
            loader=loader,
            site_url=site_url,
            asset_url=asset_url,
            render_dir=render_dir,
            repo=MinecraftAssetsRepo(
                github=Github(),
                ref=minecraft_props.ref,
                version=minecraft_props.version,
            ),
        )
