#!/usr/bin/env python3
"""Compose editable SVG screens from a frame spec. No network or dependencies."""

import argparse
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ALLOWED = {
    "svg", "title", "desc", "g", "text", "tspan", "rect", "circle",
    "ellipse", "line", "polyline", "polygon", "path",
}


def tag(name):
    return f"{{{SVG}}}{name}"


def add(parent, name, **attrs):
    return ET.SubElement(parent, tag(name), {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def text(parent, label, x, y, *, size, color, weight="normal"):
    add(parent, "text", x=x, y=y, font_size=size, font_weight=weight, fill=color,
        font_family="Noto Sans SC, PingFang SC, sans-serif").text = label


def read_svg(path):
    data = path.read_text(encoding="utf-8")
    if "<!DOCTYPE" in data or "<!ENTITY" in data:
        raise ValueError(f"{path}: SVG 外部声明不可用")
    root = ET.fromstring(data)
    if root.tag != tag("svg"):
        raise ValueError(f"{path}: 需要带 SVG 命名空间的根节点")
    for item in root.iter():
        if item.tag not in {tag(name) for name in ALLOWED}:
            raise ValueError(f"{path}: {item.tag} 不能稳定转换为原生节点")
        for key, val in item.attrib.items():
            if key.rsplit("}", 1)[-1].lower().startswith(("on", "href")) or "url(" in val.lower():
                raise ValueError(f"{path}: SVG 需要自包含且无事件处理器")
    box = [float(value) for value in root.attrib["viewBox"].replace(",", " ").split()]
    if len(box) != 4 or box[:2] != [0, 0] or any(not math.isfinite(n) or n <= 0 for n in box[2:]):
        raise ValueError(f"{path}: viewBox 需为 0 0 width height")
    return root, box[2], box[3]


def load_frame(frame, folder, catalog):
    entry = catalog.get(frame.get("template"))
    if entry is None and "template" in frame:
        raise ValueError(f"未知底稿: {frame['template']}")
    source = folder / frame["svg"] if "svg" in frame else SKILL / "assets" / entry["svg"]
    svg, width, height = read_svg(source)
    attrs = {key: value for key, value in svg.attrib.items()
             if key not in {"viewBox", "version", "width", "height"}}
    layer = ET.Element(tag("g"), attrs)
    for node in svg:
        if node.tag not in {tag("title"), tag("desc")}:
            layer.append(node)
    for name in frame.get("highlight", []):
        if entry is None or name not in entry["anchors"]:
            raise ValueError(f"未知强调位置: {name}")
        if (width, height) != (entry["width"], entry["height"]):
            raise ValueError("自定义 SVG 尺寸应与所用锚点的底稿一致")
        a = entry["anchors"][name]
        add(layer, "rect", x=a["x"], y=a["y"], width=a["width"], height=a["height"],
            rx=5, fill="none", stroke="#3568EB", stroke_width=2.5)
    return layer, width, height


def compose(config, folder):
    catalog = json.loads((SKILL / "assets/catalog.json").read_text(encoding="utf-8"))
    templates = {item["id"]: item for item in catalog["templates"]}
    for alias, target in catalog.get("aliases", {}).items():
        templates[alias] = templates[target]
    frames = config["frames"]
    columns = config.get("columns", 2)
    if not frames or type(columns) is not int or not 1 <= columns <= 4:
        raise ValueError("至少需要一帧，columns 取 1 到 4")
    loaded = [load_frame(frame, folder, templates) for frame in frames]
    padding, gap, header, row_gap = 32, 60, 64, 46
    root = ET.Element(tag("svg"))
    y, max_width = padding, 0
    for index in range(0, len(frames), columns):
        row = loaded[index:index + columns]
        x = padding
        for offset, (layer, width, height) in enumerate(row):
            frame = frames[index + offset]
            group = add(root, "g", transform=f"translate({x},{y})")
            text(group, f"{index + offset + 1:02d}  {frame['title']}", 0, 24,
                 size=24, color="#1F2735", weight="bold")
            if frame.get("caption"):
                text(group, frame["caption"], 0, 49, size=15, color="#59677B")
            screen = add(group, "g", transform=f"translate(0,{header})")
            screen.append(layer)
            if config.get("arrows", False) and offset + 1 < len(row):
                cy = header + height / 2
                add(group, "polyline", points=f"{width+13},{cy} {width+44},{cy} {width+37},{cy-6}",
                    fill="none", stroke="#3568EB", stroke_width=2, stroke_linejoin="round")
                add(group, "line", x1=width+44, y1=cy, x2=width+37, y2=cy+6,
                    stroke="#3568EB", stroke_width=2)
            x += width + gap
        max_width = max(max_width, x - gap)
        y += max(frame[2] for frame in row) + header + row_gap
    size = (math.ceil(max_width + padding), math.ceil(y - row_gap + padding))
    root.attrib.update({"width": str(size[0]), "height": str(size[1]),
                        "viewBox": f"0 0 {size[0]} {size[1]}"})
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        root = compose(json.loads(args.spec.read_text(encoding="utf-8")), args.spec.parent)
        ET.ElementTree(root).write(args.output, encoding="utf-8", xml_declaration=True)
    except (KeyError, OSError, TypeError, ValueError, ET.ParseError) as error:
        parser.exit(2, f"无法拼版：{error}\n")


if __name__ == "__main__":
    main()
