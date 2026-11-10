# 飞书画板交付

如环境已提供飞书文档与画板技能，使用它们定位文档块、获取权限和写入。以下为有 lark-cli 时的 CLI 路径。参数名以安装版本的 --help 为准。使用有目标权限的用户身份，文件路径用当前工作目录内的相对路径。

## 先检查画板能保留哪些节点

```sh
npx -y @larksuite/whiteboard-cli@0.2.13 -i ./storyboard.svg -f svg --check
npx -y @larksuite/whiteboard-cli@0.2.13 -i ./storyboard.svg -f svg -o ./preview.png
npx -y @larksuite/whiteboard-cli@0.2.13 -i ./storyboard.svg -f svg --to openapi --format json -o ./nodes.json
python3 path/to/skill/scripts/verify_native.py ./nodes.json --require-text "记录详情" --require-text "保存"
```

替换示例中的关键文案为本次需要验收的标签。打开 preview.png 逐帧目检。单个 SVG 或图片节点并不保证其内部可编辑。复杂路径可能让同组文字一起落成 SVG，即使 --check 没报错也要检查原生节点。遇到这种情况，将复杂图形与文字分组，或把复杂图形简化成基本图元，再重新转换。使用自包含 SVG，避开外部资源、脚本、filter、mask、clipPath、pattern 和复杂矩阵变换。中文需有可用字体。

## 新画板

先用文档目录或锚点找出插入位置，确定用户授权的文档和块。用户明确要新建文档时，先用飞书文档工具创建，并取新文档的目标标题块作为插入锚点。原生节点转换和预览通过后，再创建画板，避免文档里留下空白占位。

```sh
lark-cli docs +update --doc "$doc_token" --command block_insert_after \
  --block-id "$anchor_id" --content '<whiteboard type="blank"></whiteboard>' --as user
```

从返回的 document.new_blocks 取 whiteboard 的 block_token 和 block_id。若调用回执缺少 token，重新读目标位置确认。可为本次操作生成一个 UUID，网络重试时沿用同一个值。

```sh
lark-cli whiteboard +update --whiteboard-token "$board_token" \
  --input_format raw --source @./nodes.json \
  --idempotent-token "$operation_id" --as user
```

## 更新已有画板

1. 读取目标画板的 raw 与预览，记下节点 ID、位置、分组和与评论有关的对象。新增状态优先排到画板空区。需要在已有坐标系追加时，给转换后的新节点做一致的平移并检查边界和连线，避开旧画面。
2. 写前重新读取，确认目标节点、空间及编辑计划仍相符。按工具能保留原节点 ID 的方式局部修改。若工具只能追加，追加清楚标识的修订帧，或交付已校验的待导入文件。含评论的旧节点保持其锚点。只有用户明确要整板替换，且核对已保存的内容和评论影响后，才考虑覆盖。
3. 写入回执后读 raw 和可见导出。逐项确认新增节点 ID、关键文案类型、原有节点和分组关系，以及飞书文档仍挂载同一个画板。缩略图可能滞后，用当前 SVG 导出或可见画板复核。出现部分成功先查已写入节点和幂等标识。

```sh
lark-cli whiteboard +query --whiteboard-token "$board_token" \
  --output_as raw --output ./board-after.json --as user
lark-cli whiteboard +query --whiteboard-token "$board_token" \
  --output_as svg --output ./board-after.svg --as user
```

最后提供文档内画板入口，必要时附源图或预览，并说明确认了哪些节点可编辑。
