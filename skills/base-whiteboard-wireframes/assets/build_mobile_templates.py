#!/usr/bin/env python3
"""Mobile companion templates retained separately from the desktop reference set."""
from html import escape
from pathlib import Path
HERE=Path(__file__).resolve().parent
INK, MUTED, FAINT = '#1d2534', '#526078', '#78859a'
LINE, PANEL, BG, WHITE = '#dbe2ed', '#f6f8fc', '#edf1f7', '#ffffff'
BLUE, TINT = '#2860de', '#eef3ff'
WIDTH, HEIGHT = 1440,900
NAMES = ['示例数据'] * 3
STATUS = [('选项1', '#e8efff', '#345db2'), ('选项2', '#f2edf9', '#70549b'), ('选项3', '#e9f5ee', '#347055')]
PEOPLE = ['示例成员'] * 3

class Board:
    def __init__(self, key, title, scenarios, width=WIDTH, height=HEIGHT):
        self.key = key
        self.width, self.height = width, height
        self.nodes = []
        self.meta = dict(id=key, title=title, svg=f'{key}.svg', png=f'{key}.png',
                         scenarios=scenarios, width=width, height=height, anchors={})
        self.rect(0, 0, width, height, WHITE)

    def anchor(self, name, x, y, width, height):
        assert x >= 0 and y >= 0 and x + width <= self.width and y + height <= self.height, name
        self.meta['anchors'][name] = dict(x=x, y=y, width=width, height=height)

    def rect(self, x, y, w, h, fill=WHITE, stroke='none', radius=0, sw=1):
        self.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x, y, x2, y2, color=LINE, sw=1):
        self.nodes.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')

    def circle(self, x, y, r, fill=BLUE):
        self.nodes.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def text(self, x, y, value, size=15, color=INK, weight=400):
        self.nodes.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>')

    def pill(self, x, y, label, fill=TINT, ink=BLUE, w=67):
        self.rect(x, y, w, 25, fill, radius=5)
        self.text(x + 9, y + 17, label, 12, ink, 550)

    def button(self, x, y, label, primary=False, w=88, h=34):
        self.rect(x, y, w, h, BLUE if primary else WHITE, 'none' if primary else LINE, 6)
        self.text(x + 13, y + 22, label, 14, WHITE if primary else INK, 550)

    def panel(self, x, y, w, h, title, caption=''):
        self.rect(x, y, w, h, WHITE, LINE, 10)
        self.text(x + 22, y + 35, title, 18, INK, 650)
        if caption:
            self.text(x + 22, y + 62, caption, 13, MUTED)

    def write(self):
        content = '\n'.join(self.nodes)
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">\n{content}\n</svg>\n'
        (HERE / self.meta['svg']).write_text(svg, encoding='utf-8')

def dim(b, x=0, y=0, w=WIDTH, h=HEIGHT):
    b.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#34435d" opacity="0.23"/>')

def phone_grid(b):
    b.rect(0, 0, 420, 900, WHITE)
    b.text(25, 36, '9:41', 15, INK, 650)
    for i, h in enumerate((4, 6, 8, 11)):
        b.rect(326 + i * 5, 35 - h, 3, h, INK, radius=1)
    b.rect(361, 24, 28, 12, WHITE, INK, 3)
    b.rect(365, 27, 20, 6, INK, radius=2)
    b.rect(390, 28, 2, 4, INK, radius=1)
    b.text(20, 82, '‹', 27, INK, 600)
    b.text(48, 78, '数据表1', 20, INK, 650)
    for x in (378, 386, 394):
        b.circle(x, 71, 2, MUTED)
    b.line(0, 100, 420, 100)
    b.rect(0, 101, 420, 46, PANEL)
    b.rect(17, 108, 66, 30, WHITE, LINE, 5)
    b.text(32, 129, '表格', 14, BLUE, 600)
    b.text(101, 129, '看板', 14, MUTED)
    b.text(161, 129, '日历', 14, MUTED)
    b.text(224, 129, '+', 17, MUTED)
    b.text(20, 181, '+ 新增记录', 15, BLUE, 550)
    b.text(302, 181, '筛选     排序', 14, MUTED)
    b.line(0, 200, 420, 200)
    b.rect(0, 201, 420, 42, PANEL)
    for x in (35, 204, 284, 363):
        b.line(x, 202, x, 447)
    for x, label in ((48, '文本1'), (216, '单选1'), (295, '人员1')):
        b.text(x, 228, label, 13, MUTED, 600)
    b.rect(372, 206, 40, 31, TINT, radius=5)
    b.text(386, 230, '+', 21, BLUE, 600)
    for i, name in enumerate(NAMES):
        y = 243 + 68 * i
        b.line(0, y, 420, y)
        b.text(12, y + 40, i + 1, 12, FAINT)
        b.text(48, y + 40, name, 14, INK, 550 if i == 0 else 400)
        label, fill, ink = STATUS[i % 3]
        b.pill(211, y + 24, label, fill, ink, 65)
        b.text(297, y + 40, PEOPLE[i % 3], 13, MUTED)
    b.line(0, 447, 420, 447)
    b.line(0, 821, 420, 821)
    b.text(25, 860, '数据表', 14, BLUE, 600)
    b.text(137, 860, '视图', 14, MUTED)
    b.text(229, 860, '更多', 14, MUTED)
    b.rect(150, 883, 120, 5, INK, radius=2)
    b.anchor('mobile-header', 0, 44, 420, 56)
    b.anchor('view-tabs', 0, 101, 420, 46)
    b.anchor('table-header', 0, 201, 420, 42)
    b.anchor('field-add', 369, 201, 47, 42)
    b.anchor('grid-body', 0, 243, 420, 204)
    b.anchor('selected-cell', 35, 243, 169, 68)

def mobile_grid():
    b = Board('mobile-grid', '手机数据表', ['手机端表头', '新增字段', '单元格选中'], 420, 900)
    phone_grid(b)
    return b

def mobile_sheet():
    b = Board('mobile-sheet', '手机底部字段配置', ['底部弹层', '手机端字段类型配置', '保存与取消'], 420, 900)
    phone_grid(b)
    dim(b, 0, 0, 420, 900)
    b.rect(0, 345, 420, 555, WHITE, LINE, 16)
    b.rect(0, 859, 420, 41, WHITE)
    b.rect(177, 355, 66, 5, LINE, radius=2)
    b.text(20, 393, '取消', 15, MUTED)
    b.text(174, 394, '新增字段', 18, INK, 650)
    b.text(367, 393, '确定', 15, BLUE, 650)
    b.line(0, 411, 420, 411)
    for i, (label, value) in enumerate((('字段名称', '新字段'), ('字段类型', '文本'))):
        y = 442 + 104 * i
        b.text(22, y + 17, label, 15, MUTED, 550)
        b.rect(21, y + 28, 378, 44, PANEL, LINE, 7)
        b.text(35, y + 55, value, 15, FAINT if i == 2 else INK)
        if i == 1:
            b.text(373, y + 56, '›', 20, MUTED)
    b.rect(150, 883, 120, 5, INK, radius=2)
    b.anchor('bottom-sheet', 0, 345, 420, 555)
    b.anchor('sheet-actions', 14, 369, 392, 41)
    b.anchor('field-type', 21, 574, 378, 44)
    return b

def build_all():
    return [mobile_grid(),mobile_sheet()]
