from __future__ import annotations

import argparse
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import dulwich.porcelain
import jinja2
import pydantic
import pyparsing
import yaml

from .zon import loads

THIS_DIRECTORY = Path(__file__).parent.resolve()
TEMPLATE_DIRECTORY = THIS_DIRECTORY / "templates"


def main(args: list[str]) -> None:
    config = parse_args(args)
    if not config.config_file.exists():
        print(f"Config file doesnt exist. {config.config_file.resolve().as_posix()}")
        raise SystemExit(1)

    generator_configuration_text = config.config_file.read_text(encoding="utf-8")
    generator_configuration_raw = yaml.safe_load(generator_configuration_text)
    generator_configuration = GeneratorConfig.model_validate(
        generator_configuration_raw
    )

    loader = jinja2.FileSystemLoader([TEMPLATE_DIRECTORY.as_posix()])
    env = jinja2.Environment(loader=loader)

    def _(repo: Path):
        for asset in generator_configuration.assets:
            generate_assets(generator_configuration, asset, env, repo)

    if config.repo is None:
        with TemporaryDirectory() as tmp:
            with dulwich.porcelain.clone(
                source=generator_configuration.repo,
                target=tmp,
                branch=generator_configuration.target,
            ):
                _(Path(tmp))
    else:
        with dulwich.porcelain.open_repo(config.repo.as_posix()):
            _(config.repo)


def generate_assets(
    generator_configuration: GeneratorConfig,
    config: AssetConfig,
    env: jinja2.Environment,
    repository: Path,
) -> None:
    template = env.get_template(config.template)

    source = repository / config.source

    for file_path in source.glob(config.glob):
        print("Processing:", file_path.as_posix(), end="")

        file_name_no_suffix = file_path.name.split(".")[0]
        replative_path = file_path.relative_to(source)
        relative_no_suffix = replative_path.parent / file_name_no_suffix

        print(".", end="")

        destination_path = (
            Path.cwd()
            / config.destination
            / replative_path.parent
            / f"{file_name_no_suffix}.md"
        )
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        print(".", end="")

        if destination_path.exists():
            print("already exists")
            continue

        print(".", end="")

        content = file_path.read_text(encoding="utf-8")
        print(".", end="")

        zon = loads(content)
        print(".", end="")

        rendered_content = template.render(
            zon=zon,
            name=file_path.name.split(".")[0].replace("_", " ").capitalize(),
            id=f"cubyz:{relative_no_suffix.as_posix()}",
            gcfg=generator_configuration,
            cfg=config,
            relative_to_source_no_suffix=relative_no_suffix,
            extract_texture_relpath=extract_texture_relpath,
        )
        print(".", end="")

        destination_path.write_text(rendered_content, encoding="utf-8")
        print("Done")


def extract_texture_relpath(texture_id: str) -> str:
    _, path = texture_id.split(":")
    return path + ".png"


class GeneratorConfig(pydantic.BaseModel):
    repo: str
    target: str
    assets: List[AssetConfig]


class AssetConfig(pydantic.BaseModel):
    source: str
    destination: str
    template: str
    glob: str
    image_root: str


class Config(pydantic.BaseModel):
    config_file: Path
    repo: Path | None = None


def parse_args(args: list[str]) -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", type=Path)
    parser.add_argument("--repo", "-r", type=Path, default=None)
    return Config(**vars(parser.parse_args(args)))


if __name__ == "__main__":
    main(sys.argv[1:])
