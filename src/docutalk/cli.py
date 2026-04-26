from __future__ import annotations

import argparse

from docutalk.config import load_settings
from docutalk.rag import get_or_create_index


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DocuTalk utility commands")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force a full FAISS index rebuild from PDFs in data/raw.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = load_settings()
    settings.ensure_directories()

    try:
        _, built_now, chunk_count = get_or_create_index(settings, rebuild=args.rebuild)
    except FileNotFoundError as exc:
        print(str(exc))
        raise SystemExit(1) from exc

    if built_now:
        print(f"Index built successfully with {chunk_count} chunks.")
    else:
        print("Index loaded from cache in data/index.")


if __name__ == "__main__":
    main()
