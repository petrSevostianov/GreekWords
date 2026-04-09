from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_main_dir = script_dir.parent
    default_output = script_dir / "front_words.txt"

    parser = argparse.ArgumentParser(
        description=(
            "Collect unique front words from level-1 headings in Markdown cards "
            "inside the Main folder."
        )
    )
    parser.add_argument(
        "--main-dir",
        type=Path,
        default=default_main_dir,
        help="Path to the Main folder with dictionary Markdown files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help="Path to the output txt file.",
    )
    return parser.parse_args()


def collect_front_words(main_dir: Path) -> list[str]:
    seen: set[str] = set()
    fronts: list[str] = []

    for markdown_path in sorted(main_dir.glob("*.md")):
        for line in markdown_path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("# "):
                continue

            front = line[2:].strip()
            if not front or front in seen:
                continue

            seen.add(front)
            fronts.append(front)

    return fronts


def write_front_words(output_path: Path, fronts: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(fronts)
    if text:
        text += "\n"
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    main_dir = args.main_dir.resolve()
    output_path = args.output.resolve()

    fronts = collect_front_words(main_dir)
    write_front_words(output_path, fronts)

    print(f"Main dir: {main_dir}")
    print(f"Output: {output_path}")
    print(f"Unique fronts: {len(fronts)}")


if __name__ == "__main__":
    main()