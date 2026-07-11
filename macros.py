from __future__ import annotations
from pathlib import Path
import sys
import textwrap
from typing import TYPE_CHECKING

THIS_DIRECTORY = Path(__file__).parent
DATABSE_FILE = THIS_DIRECTORY / "scripts" / "assets.yml"

sys.path.append(THIS_DIRECTORY.as_posix())

from scripts.assetgen2 import ENV, AssetDatabase, Id

if TYPE_CHECKING:
    from zensical.extensions.macros import MacroEnv


def define_env(env: MacroEnv):
    db = AssetDatabase.load_yaml(DATABSE_FILE.read_text(encoding="utf-8"))

    @env.macro
    def item_infobox(id_string: str):
        id = Id.from_str(id_string)

        if id not in db.items:
            return ""

        item = db.items[id]
        template = ENV.get_template("item_infobox.jinja2.md")
        infobox = template.render(item=item)

        return textwrap.indent(infobox, prefix="    ")

    @env.macro
    def block_infobox(id_string: str):
        id = Id.from_str(id_string)

        if id not in db.blocks:
            return ""

        block = db.blocks[id]
        template = ENV.get_template("block_infobox.jinja2.md")
        infobox = template.render(block=block)

        return textwrap.indent(infobox, prefix="    ")
