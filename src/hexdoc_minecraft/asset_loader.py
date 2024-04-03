from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Mapping

import more_itertools
from hexdoc.core import ResourceLocation
from hexdoc.minecraft.assets import (
    HexdocAssetLoader,
    ImageTexture,
    ItemTexture,
    PNGTexture,
)
from hexdoc.minecraft.assets.items import SingleItemTexture
from yarl import URL

from .minecraft_assets import MinecraftAssetsRepo


@dataclass(kw_only=True)
class MinecraftAssetLoader(HexdocAssetLoader):
    repo: MinecraftAssetsRepo

    @cached_property
    def fallbacks(self) -> Mapping[ResourceLocation, ItemTexture]:
        texture_content = self.repo.texture_content()
        return {
            value.name: SingleItemTexture(
                inner=PNGTexture(url=URL(value.texture), pixelated=True)
            )
            for value in texture_content
            if value.texture
        }

    def find_image_textures(self) -> Iterable[tuple[ResourceLocation, ImageTexture]]:
        # export all textures, but only yield what's in minecraft_assets
        more_itertools.consume(super().find_image_textures())
        yield from self.repo.scrape_image_textures()

    def load_item_models(self):
        for item_id, model in super().load_item_models():
            if model.parent and model.parent.path.startswith("builtin"):
                continue
            yield item_id, model

    def fallback_texture(self, item_id: ResourceLocation) -> ItemTexture | None:
        return self.fallbacks.get(item_id)
