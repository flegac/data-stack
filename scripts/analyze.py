import os
import subprocess
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_PATH / "docs/generated"

IGNORED = [
    "tests",
    "__pycache__",
    ".venv",
    "site-packages",
    "__init__.py",
    "docs",
    "scripts",
]


def analyze_project(project_toml: Path):
    print(f"{project_toml.parent}")
    generate_dependencies(project_toml)
    generate_structure(project_toml)


def generate_structure(project_toml: Path):
    project_dir = project_toml.parent
    project_name = project_dir.name
    output_dir = ROOT_PATH / "docs/generated/structure"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / project_dir.with_suffix(".md").name

    if os.name == "nt":  # Windows
        command = f'tree /F /A "{project_name}"'
    else:  # Unix
        command = f'tree -I "{"|".join(IGNORED)}" --noreport -P "*.py" {project_name}'

    dump_command_result(
        command=command,
        execution_dir=project_dir.parent,
        output_file=output_file,
    )


def generate_dependencies(project_toml: Path):
    project_dir = project_toml.parent
    project_name = project_dir.name
    output_dir = ROOT_PATH / "docs/generated/dependencies"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / project_dir.with_suffix(".md").name
    dump_command_result(
        command=f"uv tree --package {os.path.basename(project_name)}",
        execution_dir=project_dir,
        output_file=output_file,
    )


def dump_command_result(command: str, execution_dir: Path, output_file: Path):
    output_dir = output_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    os.chdir(execution_dir)
    encoding = "utf-8"
    if os.name == "nt":
        encoding = "cp1252"
    with output_file.open("w", encoding="utf-8") as _:
        _.write("```\n")
        _.flush()
        process = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            check=False,
            encoding=encoding,
        )
        result = str(process.stdout)
        result = result.replace(" ", " ")
        result = result.encode(encoding).decode("utf-8", errors="replace")
        _.write(result)
        _.flush()
        _.write("```\n")


def main():
    generate_docs(
        root_dir=ROOT_PATH,
        output_dir=OUTPUT_DIR / "doc",
    )
    # dump_command_result(
    #     command="uv pip tree",
    #     execution_dir=ROOT_PATH,
    #     output_file=ROOT_PATH / "docs/generated/pip-tree.md",
    # )
    # for project_toml in ROOT_PATH.glob("**/pyproject.toml"):
    #     analyze_project(project_toml)


def generate_docs(root_dir: Path, output_dir: Path) -> None:
    root_dir = root_dir.absolute()
    output_dir = output_dir.absolute()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all Python modules (excluding those starting with _)
    modules = []

    files = [
        *root_dir.rglob("adapters/**/*.py"),
        *root_dir.rglob("projects/**/*.py"),
    ]

    accepted = [
        "entities",
        "service",
        "repository",
    ]

    for py_file in files:
        if py_file.name.startswith("_"):
            continue
        if "test" in py_file.name:
            continue

        is_accepted = any([label in str(py_file) for label in accepted])
        if not is_accepted:
            continue

        modules.append(str(py_file))

    modules_str = " ".join(modules)
    subprocess.run(
        f"pdoc --no-show-source --search --output-dir {output_dir} {modules_str}",
        shell=True,
        check=True,
        capture_output=True,
        text=True,
    )


if __name__ == "__main__":
    main()
