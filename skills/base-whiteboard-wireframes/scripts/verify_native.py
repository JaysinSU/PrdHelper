#!/usr/bin/env python3
"""Check that required labels survived SVG conversion as editable text nodes."""

import argparse
import json
from collections import Counter
from pathlib import Path


def read_nodes(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        if isinstance(value.get("nodes"), list):
            return value["nodes"]
        if "data" in value:
            return read_nodes(value["data"])
    raise ValueError("找不到画板原生节点列表")


def editable_text(node):
    content = node.get("text", {})
    if isinstance(content, str):
        return content
    return content.get("text", "") if isinstance(content, dict) else ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("--require-text", action="append", default=[], help="精确匹配可编辑文字，可重复传入")
    args = parser.parse_args()
    try:
        nodes = read_nodes(json.loads(args.raw.read_text(encoding="utf-8")))
        counts = Counter(node.get("type") for node in nodes)
        labels = {editable_text(node).strip() for node in nodes if node.get("type") == "text_shape"}
        labels.discard("")
        missing = [label for label in args.require_text if label.strip() not in labels]
        print(json.dumps({"nodes": len(nodes), "types": dict(counts),
                          "missing_editable_text": missing}, ensure_ascii=False))
        return int(not labels or bool(missing))
    except (OSError, ValueError, AttributeError) as error:
        parser.exit(2, f"无法读取画板节点：{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
