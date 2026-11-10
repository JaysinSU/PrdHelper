# Base 飞书画板线稿

从一段需求或 PRD 出发，用内置 Base 底稿绘制关键界面和交互状态，再写入飞书云文档的可编辑画板。底稿是虚构界面，包含可改的 SVG 和可快速预览的 PNG。

## 交给 AI

下载或解压后，把整个 `base-whiteboard-wireframes` 目录交给 AI，保留 `assets/`、`references/` 和 `scripts/`。也可以把目录放到 Codex 的 `skills` 目录，再用 `$base-whiteboard-wireframes` 调用。

> 先读这个目录里的 SKILL.md。根据我的需求画两帧，沿用 Base 桌面表格底稿，标出字段类型入口和新增字段确认后的状态。把可编辑画板插入我给的飞书文档「产品方案」下。

如果已有画板，把目标文档和画板位置一并给 AI。有修改权限的飞书连接或 lark-cli 可以完成云端写入。在本地检查线稿只需要 Python 3，转换与预览另需 Node.js 和 whiteboard-cli。

## 底稿和示例

- [底稿目录](assets/catalog.json)记录每个场景的 SVG、PNG 和可标注区域。
- [编帧方法](references/storyboarding.md)包含新字段、富内容编辑、Excel 导入、表与视图描述、表单和仪表盘的用法。
- [飞书画板交付](references/feishu-whiteboard.md)覆盖原生节点转换、指定位置插入、已有画板的局部修改和读回验收。

在技能目录运行下面的示例，把两张底稿放在同一幅 SVG 中。修改每帧的 `template`、`title`、`caption` 和 `highlight` 即可换场景。需要修改控件时，用 `svg` 指定相对于配置文件的编辑后源图。

```sh
python3 scripts/compose.py examples/field-entry.json ./storyboard.svg
npx -y @larksuite/whiteboard-cli@0.2.13 -i ./storyboard.svg -f svg --to openapi --format json -o ./nodes.json
python3 scripts/verify_native.py ./nodes.json --require-text "搜索字段类型" --require-text "文本"
```

技能入口见 [SKILL.md](SKILL.md)。
