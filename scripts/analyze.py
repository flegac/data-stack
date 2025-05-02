import os
import subprocess
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent


def analyze_project(project_toml: Path):
    project_dir = project_toml.parent
    output_dir = ROOT_PATH / "docs/generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / project_dir.name
    print(f"{project_dir} -> {output_file}")

    generate_tree(project_toml)


def generate_tree(project_toml: Path):
    project_dir = project_toml.parent

    output_dir = ROOT_PATH / "docs/generated/tree"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / project_dir.with_suffix(".pip-tree.md").name

    os.chdir(project_dir)
    with output_file.open("w") as _:
        _.write("```\n")
        _.flush()
        subprocess.run(
            ["uv", "tree", "--package", os.path.basename(project_dir.name)],
            text=True,
            stdout=_,
        )
        _.flush()
        _.write("```\n")


def generate_pip_tree(project_dir: Path):
    output_dir = ROOT_PATH / "docs/generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "pip-tree.md"

    os.chdir(project_dir)
    with output_file.open("w") as _:
        subprocess.run(
            ["uv", "pip", "tree"],
            text=True,
            stdout=_,
        )


def main():
    generate_pip_tree(ROOT_PATH)
    for project_toml in ROOT_PATH.glob("**/pyproject.toml"):
        analyze_project(project_toml)


if __name__ == "__main__":
    main()
