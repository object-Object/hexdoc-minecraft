from importlib.resources import Package

from hexdoc.plugin import (
    HookReturn,
    ModPlugin,
    ModPluginImpl,
    VersionedModPlugin,
    hookimpl,
)

from .__gradle_version__ import FULL_VERSION, GRADLE_VERSION
from .__version__ import PY_VERSION


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
