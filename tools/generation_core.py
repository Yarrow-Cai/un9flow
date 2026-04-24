from __future__ import annotations

from pathlib import Path


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def replace_fields(template_text: str, fields: dict[str, str]) -> str:
    rendered = template_text
    for key, value in fields.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered
