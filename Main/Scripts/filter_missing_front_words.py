from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=(
            "Filter a *.words.txt file and keep only source forms that are not "
            "already present among Main card fronts."
        )
    )
    parser.add_argument(
        "words_file",
        type=Path,
        help="Path to the input *.words.txt file.",
    )
    parser.add_argument(
        "--front-words",
        type=Path,
        default=script_dir / "front_words.txt",
        help="Path to Main/Scripts/front_words.txt.",
    )
    return parser.parse_args()


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]


def filter_missing_words(words: list[str], known_fronts: set[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    for word in words:
        if not word or word in known_fronts or word in seen:
            continue

        seen.add(word)
        result.append(word)

    return result


def write_lines(path: Path, lines: list[str]) -> None:
    text = "\n".join(lines)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    words_file = args.words_file.resolve()
    front_words_file = args.front_words.resolve()

    words = read_lines(words_file)
    known_fronts = set(read_lines(front_words_file))
    missing_words = filter_missing_words(words, known_fronts)
    write_lines(words_file, missing_words)

    print(f"Words file: {words_file}")
    print(f"Front words: {front_words_file}")
    print(f"Remaining words: {len(missing_words)}")


if __name__ == "__main__":
    main()