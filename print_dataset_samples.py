#!/usr/bin/env python3
"""Print a few sample items from the LTspice Unsloth dataset JSON file."""

import argparse
import json
from pathlib import Path


DEFAULT_PATH = Path("/home/brosnan/books/circuits/ltspice_unsloth_dataset.json")


def truncate(text: str, max_len: int = 180000) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load a JSON dataset and print a few sample items."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_PATH,
        help=f"Path to dataset JSON (default: {DEFAULT_PATH})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="How many items to print (default: 3)",
    )
    args = parser.parse_args()

    with args.path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError("Expected top-level JSON array.")

    print(f"Loaded {len(data)} items from: {args.path}")
    print()

    for i, item in enumerate(data[: max(args.count, 0)], start=1):
        if not isinstance(item, dict):
            print(f"[{i}] Non-dict item: {type(item).__name__}")
            print()
            continue

        item_id = item.get("id", "<missing id>")
        question = item.get("question", "")
        answer = item.get("answer", "")

        print(f"[{i}] id: {item_id}")
        print("    question:")
        print(truncate(str(question)))
        print("    answer:")
        print(truncate(str(answer)))
        print()


if __name__ == "__main__":
    main()
