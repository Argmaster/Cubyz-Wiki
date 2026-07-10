from __future__ import annotations
import argparse
from pathlib import Path
import sys
from typing import ClassVar, Dict

import pydantic

from . import zon


def main(args: list[str]) -> None:
    config = parse_args(args)

    if config.repo is not None and config.repo.exists():
        rebuild_metadata(config)


def parse_args(args: list[str]) -> CliArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo", "-r", type=Path, default=None, help="Path to local Cubyz repo clone."
    )
    parser.add_argument("--db", type=Path, default=None, help="Path to local asset database.")
    return CliArgs(**vars(parser.parse_args(args)))


class CliArgs(pydantic.BaseModel):
    repo: Path | None = None
    meta: Path | None = None


def rebuild_metadata(args: CliArgs) -> None:
    assets = AssetDatabase()
    rebuild_items(args, assets)
    # rebuild_blocks(args, assets)


def rebuild_items(args: CliArgs, assets: AssetDatabase):
    assert args.repo is not None
    items_directory = args.repo / Item.ASSET_PATH

    for file in items_directory.glob("**/*.zon"):
        content = file.read_text(encoding="utf-8")
        zon.loads(content)


class Id(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)

    string: str

    @property
    def path(self) -> str:
        return self.string.split(":")[1]


class Item(pydantic.BaseModel):
    ASSET_PATH: ClassVar[str] = "assets/cubyz/items"
    TEXTURE_PATH: ClassVar[str] = "assets/cubyz/items/textures"

    tags: list[str]
    material: Material
    texture: Texture | None
    block_id: Id | None


class Material(pydantic.BaseModel):
    durability: float
    massDamage: float
    hardnessDamage: float
    swingSpeed: float


class Block(pydantic.BaseModel):
    ASSET_PATH: ClassVar[str] = "assets/cubyz/blocks"
    TEXTURE_PATH: ClassVar[str] = "assets/cubyz/blocks/textures"

    tags: list[str]
    blockHealth: int
    blockResistance: int
    item_id: Id
    ore: Ore
    texture: Texture | None
    textures: list[Texture | None]
    texture_top: Texture | None
    texture_bottom: Texture | None
    texture_front: Texture | None
    texture_left: Texture | None
    texture_right: Texture | None
    isInteracive: bool


class Texture(pydantic.BaseModel):
    path: str


class Ore(pydantic.BaseModel):
    max_height: int
    min_height: int


class AssetDatabase(pydantic.BaseModel):
    items: Dict[Id, Item] = pydantic.Field(default_factory=dict)
    blocks: Dict[Id, Block] = pydantic.Field(default_factory=dict)


if __name__ == "__main__":
    main(sys.argv[1:])
