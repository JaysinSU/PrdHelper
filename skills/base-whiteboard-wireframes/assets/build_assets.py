#!/usr/bin/env python3
"""Build synthetic Base SVG underlays. --render also creates matching PNGs."""
from html import escape
from pathlib import Path
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
INK, MUTED, FAINT = '#1d2534', '#526078', '#78859a'
LINE, PANEL, BG, WHITE = '#dbe2ed', '#f6f8fc', '#edf1f7', '#ffffff'
BLUE, TINT = '#2860de', '#eef3ff'
WIDTH, HEIGHT = 1440, 900
HEADERS = ['项目名称', '状态', '负责人', '截止日期', '备注']
NAMES = ['更新交付清单', '整理现场反馈', '核对项目排期', '准备验收材料', '跟进测试结果', '整理交接文档', '检查更新说明', '同步处理记录']
STATUS = [('进行中', '#e8efff', '#345db2'), ('待处理', '#f2edf9', '#70549b'), ('已完成', '#e9f5ee', '#347055')]
PEOPLE = ['成员 A', '成员 B', '成员 C']
COLS = [264, 318, 604, 765, 919, 1079, 1351, 1413]


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


def frame(b, active='表格', tools=('筛选', '分组', '排序', '行高')):
    b.rect(0, 0, WIDTH, 58, WHITE)
    b.line(0, 58, WIDTH, 58)
    b.rect(20, 17, 24, 24, BLUE, radius=6)
    b.line(26, 25, 38, 25, WHITE, 2)
    b.line(26, 30, 38, 30, WHITE, 2)
    b.line(26, 35, 35, 35, WHITE, 2)
    b.text(57, 36, '示例空间  /  项目协作台', 17, INK, 650)
    b.button(1251, 12, '分享', True, 70)
    b.text(1341, 36, '帮助', 14, MUTED)
    b.circle(1400, 29, 13, BG)
    b.text(1395, 34, 'A', 12, MUTED, 650)
    b.rect(0, 59, 242, HEIGHT - 59, PANEL)
    b.line(242, 59, 242, HEIGHT)
    b.text(21, 96, '数据表', 15, INK, 650)
    b.text(205, 96, '+', 18, BLUE, 650)
    for i, name in enumerate(('项目跟进', '成员清单', '交付记录')):
        y = 116 + i * 45
        if i == 0:
            b.rect(12, y, 217, 36, TINT, radius=6)
        b.rect(25, y + 11, 13, 13, WHITE, BLUE if i == 0 else FAINT, 2)
        b.line(25, y + 16, 38, y + 16, BLUE if i == 0 else FAINT)
        b.text(49, y + 23, name, 14, BLUE if i == 0 else MUTED, 550 if i == 0 else 400)
    b.line(12, 259, 226, 259)
    b.text(22, 292, '新增数据表', 14, MUTED)
    b.rect(242, 59, WIDTH - 242, 45, PANEL)
    b.line(242, 104, WIDTH, 104)
    for i, tab in enumerate(('表格', '看板', '日历', '甘特图', '画册', '表单')):
        x = 263 + i * 77
        if tab == active:
            b.rect(x, 67, 67, 29, WHITE, LINE, 5)
        b.text(x + 12, 87, tab, 14, BLUE if tab == active else MUTED, 550 if tab == active else 400)
    b.text(736, 88, '+', 17, MUTED)
    b.button(263, 115, '+ 新增记录', True, 110, 33)
    for i, name in enumerate(tools):
        b.text(399 + i * 75, 137, name, 14, MUTED)
    b.text(1294, 137, '搜索记录', 14, MUTED)
    b.circle(1278, 131, 5, WHITE)
    b.line(1275, 127, 1281, 133, MUTED, 1.4)
    b.line(242, 160, WIDTH, 160)
    b.anchor('sidebar', 0, 59, 242, 841)
    b.anchor('view-tabs', 243, 59, 1197, 45)
    b.anchor('toolbar', 243, 105, 1197, 55)
    b.anchor('view-canvas', 243, 161, 1197, 738)


def grid(b, select=False):
    frame(b)
    b.rect(264, 176, 1149, 414, WHITE, LINE, 8)
    b.rect(265, 177, 1147, 41, PANEL)
    for x in COLS[1:-1]:
        b.line(x, 177, x, 590)
    for i in range(9):
        y = 218 + i * 41
        b.line(264, y, 1413, y)
    b.rect(282, 191, 13, 13, WHITE, FAINT, 2)
    for i, name in enumerate(HEADERS):
        b.text(COLS[i + 1] + 15, 202, name, 14, MUTED, 550)
    b.text(1377, 204, '+', 20, BLUE, 550)
    for i, name in enumerate(NAMES):
        y = 218 + i * 41
        b.text(284, y + 26, i + 1, 13, FAINT)
        b.text(333, y + 26, name, 15, INK, 550 if i == 0 else 400)
        label, fill, ink = STATUS[i % 3]
        b.pill(619, y + 8, label, fill, ink)
        b.text(782, y + 26, PEOPLE[i % 3], 14, MUTED)
        b.text(936, y + 26, f'2026-05-{12 + i:02d}', 14, MUTED)
        b.text(1094, y + 26, ('确认最新版本', '待补充记录', '—')[i % 3], 14, MUTED)
    b.text(283, 573, '+ 新增记录', 14, FAINT)
    if select:
        b.rect(1080, 219, 270, 39, 'none', BLUE, 2, 2)
        b.rect(1346, 254, 5, 5, BLUE)
    b.anchor('table-header', 264, 176, 1149, 42)
    b.anchor('field-add', 1351, 176, 62, 42)
    b.anchor('grid-body', 264, 218, 1149, 328)
    b.anchor('selected-cell', 1079, 218, 272, 41)


def desktop_grid():
    b = Board('desktop-grid', '桌面数据表', ['表头、字段、单元格与批量操作'])
    grid(b, True)
    return b


def field_picker():
    b = Board('field-picker', '字段类型选择', ['新增字段', '替换字段类型'])
    grid(b)
    b.rect(1105, 217, 307, 470, WHITE, LINE, 9)
    b.rect(1119, 229, 279, 34, PANEL, LINE, 6)
    b.text(1133, 251, '搜索字段类型', 14, FAINT)
    b.text(1125, 286, '常规', 13, FAINT, 550)
    for i, (glyph, label) in enumerate((('A', '文本'), ('#', '数字'), ('◉', '单选'), ('✓', '多选'), ('○', '人员'), ('□', '日期'), ('↗', '超链接'), ('+', '附件'))):
        y = 296 + 32 * i
        b.rect(1120, y, 278, 30, TINT if i == 0 else WHITE, radius=4)
        b.text(1131, y + 20, glyph, 15, BLUE if i == 0 else MUTED, 650)
        b.text(1157, y + 20, label, 14, INK, 550 if i == 0 else 400)
    b.line(1120, 564, 1398, 564)
    b.text(1125, 585, '高级', 13, FAINT, 550)
    b.text(1131, 614, 'ƒ', 15, MUTED, 650)
    b.text(1157, 614, '公式', 14)
    b.text(1131, 646, '↔', 15, MUTED, 650)
    b.text(1157, 646, '关联记录', 14)
    b.anchor('field-picker', 1105, 217, 307, 470)
    b.anchor('field-picker-option', 1120, 296, 278, 30)
    return b


def dim(b, x=0, y=0, w=WIDTH, h=HEIGHT):
    b.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#34435d" opacity="0.23"/>')


def field_config():
    b = Board('field-config', '字段配置', ['修改字段标题', '设置字段类型、默认值和选项'])
    grid(b)
    b.panel(1007, 219, 405, 386, '字段配置', '配置所选字段在当前数据表中的表现')
    b.text(1376, 251, '×', 20, MUTED)
    for i, (label, value) in enumerate((('字段名称', '备注'), ('字段类型', '文本'), ('默认值', '请输入默认值'))):
        y = 299 + 70 * i
        b.text(1029, y + 9, label, 13, MUTED, 550)
        b.rect(1029, y + 18, 359, 37, PANEL if i == 2 else WHITE, LINE, 5)
        b.text(1040, y + 41, value, 14, FAINT if i == 2 else INK)
        if i == 1:
            b.text(1358, y + 40, '⌄', 16, MUTED)
    b.line(1008, 546, 1411, 546)
    b.button(1209, 557, '取消', False, 76)
    b.button(1306, 557, '确定', True, 82)
    b.anchor('field-config', 1007, 219, 405, 386)
    b.anchor('field-type', 1029, 387, 359, 37)
    b.anchor('default-value', 1029, 457, 359, 37)
    b.anchor('field-config-actions', 1195, 551, 196, 45)
    return b


def record_detail():
    b = Board('record-detail', '记录详情侧栏', ['查看记录', '在详情中编辑字段', '展开编辑'])
    grid(b, True)
    b.rect(864, 58, 576, 842, WHITE, LINE)
    b.text(892, 96, '记录详情', 15, MUTED, 600)
    b.text(1263, 95, '上一条   下一条', 13, MUTED)
    b.text(1399, 97, '×', 19, MUTED)
    b.line(865, 113, 1439, 113)
    b.text(892, 165, NAMES[0], 25, INK, 650)
    b.text(892, 208, '详情', 14, BLUE, 650)
    b.text(958, 208, '活动', 14, MUTED)
    b.line(890, 220, 1410, 220)
    b.line(891, 220, 928, 220, BLUE, 2)
    for i, (name, value) in enumerate(zip(HEADERS[1:], ('进行中', '成员 A', '2026-05-12', '确认最新版本'))):
        y = 268 + i * 54
        b.text(893, y, name, 14, MUTED)
        if i == 0:
            b.pill(1025, y - 19, value)
        else:
            b.text(1029, y, value, 15, INK)
        b.line(889, y + 24, 1414, y + 24)
    b.text(891, 496, '+ 新增字段', 14, BLUE)
    b.anchor('detail-panel', 864, 58, 576, 842)
    b.anchor('record-title', 890, 128, 519, 46)
    b.anchor('detail-fields', 889, 228, 525, 229)
    b.anchor('detail-target-field', 889, 401, 525, 56)
    return b


def editor_modal():
    b = Board('editor-modal', '居中编辑弹窗', ['展开编辑', '输入长内容', '保存与取消'])
    grid(b, True)
    dim(b)
    b.panel(335, 151, 770, 568, '编辑备注', '项目跟进  /  更新交付清单')
    b.text(1068, 184, '×', 21, MUTED)
    b.rect(358, 227, 724, 391, WHITE, LINE, 7)
    b.rect(359, 228, 722, 45, PANEL)
    b.line(359, 273, 1080, 273)
    for x, label in ((376, '正文  ⌄'), (473, 'B'), (516, 'I'), (559, 'U'), (603, '• 列表'), (684, '添加链接'), (782, '+ 插入')):
        b.text(x, 257, label, 15, MUTED, 650 if label in ('B', 'I', 'U') else 400)
    b.text(383, 312, '确认最新版本', 18, INK, 600)
    b.text(383, 347, '请在提交前核对交付清单及附件。', 15, MUTED)
    b.line(336, 643, 1104, 643)
    b.button(893, 662, '取消', False, 84)
    b.button(992, 662, '保存', True, 88)
    b.anchor('editor-modal', 335, 151, 770, 568)
    b.anchor('editor-toolbar', 359, 228, 722, 45)
    b.anchor('editor-content', 359, 274, 722, 343)
    b.anchor('editor-actions', 879, 650, 203, 51)
    return b


def kanban():
    b = Board('kanban', '看板视图', ['状态分组', '卡片字段', '卡片移动'])
    frame(b, '看板', ('分组', '筛选', '排序', '卡片设置'))
    for i, (label, fill, ink) in enumerate(STATUS):
        x = 264 + i * 385
        b.rect(x, 176, 367, 693, PANEL, LINE, 8)
        b.pill(x + 15, 191, label, fill, ink, 72)
        b.text(x + 102, 209, str(3 if i < 2 else 2), 13, FAINT)
        b.text(x + 324, 207, '+', 19, MUTED)
        for j, name in enumerate(NAMES[i::3]):
            y = 231 + j * 137
            b.rect(x + 13, y, 341, 122, WHITE, LINE, 7)
            b.text(x + 29, y + 29, name, 16, INK, 650)
            b.text(x + 29, y + 59, '负责人', 13, FAINT)
            b.text(x + 103, y + 59, PEOPLE[i], 14)
            b.text(x + 29, y + 89, '截止日期', 13, FAINT)
            b.text(x + 103, y + 89, f'2026-05-{12 + i + j:02d}', 14, MUTED)
    b.anchor('kanban-group', 264, 176, 367, 693)
    b.anchor('kanban-card', 277, 231, 341, 122)
    b.anchor('card-field', 292, 307, 305, 26)
    return b


def calendar():
    b = Board('calendar', '日历视图', ['日历事件', '日期筛选', '日程预览'])
    frame(b, '日历', ('筛选', '日历设置'))
    b.text(270, 204, '2026 年 5 月', 21, INK, 650)
    for x, label in ((436, '‹'), (477, '›'), (523, '今天')):
        b.button(x, 179, label, False, 35 if label != '今天' else 62)
    b.button(1325, 179, '月  ⌄', False, 79)
    x0, y0, cw, ch = 265, 228, 164, 113
    b.rect(x0, y0, cw * 7, 35 + ch * 5, WHITE, LINE, 7)
    b.rect(x0 + 1, y0 + 1, cw * 7 - 2, 34, PANEL)
    for i, weekday in enumerate(('一', '二', '三', '四', '五', '六', '日')):
        x = x0 + cw * i
        if i:
            b.line(x, y0, x, y0 + 35 + ch * 5)
        b.text(x + 14, y0 + 23, f'周{weekday}', 14, MUTED, 550)
    days = [27, 28, 29, 30] + list(range(1, 32))
    for row in range(5):
        y = y0 + 35 + row * ch
        b.line(x0, y, x0 + cw * 7, y)
        for col in range(7):
            i = row * 7 + col
            x = x0 + col * cw
            b.text(x + 14, y + 24, days[i], 14, FAINT if i < 4 else INK)
            if i in (8, 11, 15, 17, 23, 27):
                b.rect(x + 10, y + 34, 143, 25, TINT, radius=4)
                b.rect(x + 10, y + 35, 3, 23, BLUE, radius=1)
                b.text(x + 19, y + 52, NAMES[(i - 8) % len(NAMES)], 12, BLUE)
    b.anchor('calendar-header', 266, 174, 1141, 49)
    b.anchor('calendar-day', 429, 376, 164, 113)
    b.anchor('calendar-event', 439, 410, 143, 25)
    return b


def gantt():
    b = Board('gantt', '甘特图视图', ['时间条', '左侧表格', '进度视图'])
    frame(b, '甘特图', ('筛选', '分组', '排序', '时间范围'))
    b.rect(264, 179, 1148, 596, WHITE, LINE, 7)
    b.rect(265, 180, 1146, 62, PANEL)
    b.text(282, 216, '项目名称', 14, MUTED, 650)
    b.text(555, 201, '2026 年 5 月', 15, INK, 650)
    for i in range(12):
        x = 533 + i * 73
        b.line(x, 207 if i else 180, x, 774)
        b.text(x + 24, 231, str(i + 11), 13, FAINT)
    for i, name in enumerate(NAMES):
        y = 242 + i * 59
        b.line(265, y, 1411, y)
        b.text(282, y + 36, str(i + 1), 13, FAINT)
        b.text(317, y + 36, name, 15, INK, 550 if i == 0 else 400)
        x = 543 + (i * 2 % 7) * 73
        length = 128 + (i % 3) * 73
        _, fill, ink = STATUS[i % 3]
        b.rect(x, y + 16, length, 29, fill, radius=6)
        b.text(x + 12, y + 36, name, 13, ink, 550)
    b.anchor('gantt-field-pane', 264, 180, 269, 595)
    b.anchor('gantt-time-axis', 533, 180, 878, 62)
    b.anchor('gantt-task-bar', 543, 258, 128, 29)
    return b


def gallery():
    b = Board('gallery', '画册视图', ['画册卡片', '卡片封面与字段'])
    frame(b, '画册', ('筛选', '排序', '卡片设置'))
    for i, name in enumerate(NAMES[:6]):
        x = 264 + (i % 3) * 383
        y = 176 + (i // 3) * 333
        b.rect(x, y, 362, 312, WHITE, LINE, 8)
        b.rect(x + 1, y + 1, 360, 143, ('#eff4ff', '#f0f4fa', '#f3f0fa')[i % 3], radius=7)
        b.rect(x + 146, y + 47, 70, 51, WHITE, LINE, 6)
        b.circle(x + 160, y + 60, 5, FAINT)
        b.line(x + 154, y + 86, x + 176, y + 66, FAINT, 2)
        b.line(x + 176, y + 66, x + 195, y + 85, FAINT, 2)
        b.line(x + 195, y + 85, x + 205, y + 74, FAINT, 2)
        b.text(x + 17, y + 178, name, 17, INK, 650)
        label, fill, ink = STATUS[i % 3]
        b.pill(x + 17, y + 195, label, fill, ink)
        b.text(x + 17, y + 251, '负责人', 13, FAINT)
        b.text(x + 105, y + 251, PEOPLE[i % 3], 14, INK)
        b.text(x + 17, y + 284, '截止日期', 13, FAINT)
        b.text(x + 105, y + 284, f'2026-05-{12 + i:02d}', 14, MUTED)
    b.anchor('gallery-card', 264, 176, 362, 312)
    b.anchor('card-cover', 265, 177, 360, 143)
    b.anchor('card-field', 279, 432, 328, 35)
    return b


def form():
    b = Board('form', '表单与问卷预览', ['字段转为题目', '填写', '必填提示', '提交'])
    b.rect(0, 0, WIDTH, HEIGHT, BG)
    b.rect(0, 0, WIDTH, 62, WHITE)
    b.line(0, 62, WIDTH, 62)
    b.text(25, 39, '‹  项目协作台  /  表单', 17, INK, 650)
    b.pill(1221, 19, '预览模式', TINT, BLUE, 81)
    b.text(1322, 38, '关闭预览', 14, MUTED)
    b.panel(351, 103, 738, 697, '项目反馈收集', '请填写项目反馈，便于团队跟进。')
    b.line(352, 186, 1088, 186)
    for y, label, value, tall in ((216, '项目名称', '请输入项目名称', 39), (320, '问题描述', '请输入反馈内容', 125), (505, '优先级', '请选择', 39)):
        b.text(380, y + 15, label, 16, INK, 600)
        if y != 505:
            b.text(463, y + 14, '*', 16, '#c74c56', 650)
        b.rect(379, y + 32, 680, tall, WHITE, LINE, 6)
        b.text(391, y + 56, value, 14, FAINT)
    b.text(379, 638, '补充材料', 16, INK, 600)
    b.button(379, 652, '+ 添加文件', False, 112)
    b.button(379, 729, '提交', True, 106)
    b.anchor('form-header', 352, 104, 736, 82)
    b.anchor('form-question', 375, 315, 688, 166)
    b.anchor('form-attachment', 376, 615, 243, 81)
    b.anchor('form-submit', 379, 729, 106, 34)
    return b


def app_dashboard():
    b = Board('app-dashboard', '应用与仪表盘布局', ['列表组件', '图表组件', '配置与数据展示'])
    b.rect(0, 0, WIDTH, HEIGHT, BG)
    b.rect(0, 0, WIDTH, 62, WHITE)
    b.line(0, 62, WIDTH, 62)
    b.text(24, 40, '项目协作台  /  应用', 17, INK, 650)
    b.button(1200, 14, '配置', False, 86)
    b.button(1311, 14, '发布', True, 88)
    b.rect(0, 63, 229, HEIGHT - 63, PANEL)
    b.line(229, 62, 229, HEIGHT)
    for i, label in enumerate(('项目概览', '进度管理', '问题清单')):
        y = 94 + i * 43
        b.rect(15, y, 198, 34, TINT if i == 0 else PANEL, radius=5)
        b.text(29, y + 22, label, 15, BLUE if i == 0 else MUTED, 550)
    b.text(253, 109, '项目概览', 22, INK, 650)
    for i, (label, value) in enumerate((('记录总数', '24'), ('进行中', '8'), ('已完成', '12'))):
        x = 253 + i * 392
        b.panel(x, 138, 373, 111, label)
        b.text(x + 22, 223, value, 29, BLUE, 650)
    b.panel(253, 269, 721, 445, '项目列表', '数据来源  /  项目跟进')
    b.rect(268, 353, 691, 40, PANEL)
    for x, label in ((285, '项目名称'), (574, '状态'), (727, '负责人'), (839, '截止日期')):
        b.text(x, 379, label, 14, MUTED, 550)
    for i, name in enumerate(NAMES[:5]):
        y = 395 + i * 49
        b.line(268, y, 959, y)
        b.text(285, y + 30, name, 15)
        label, fill, ink = STATUS[i % 3]
        b.pill(574, y + 10, label, fill, ink)
        b.text(727, y + 30, PEOPLE[i % 3], 14, MUTED)
        b.text(839, y + 30, f'2026-05-{12 + i:02d}', 14, MUTED)
    b.panel(991, 269, 419, 445, '状态分布', '按记录数统计')
    for i, (label, fill, ink) in enumerate(STATUS):
        y = 394 + i * 86
        b.text(1016, y, label, 14, MUTED)
        b.rect(1016, y + 12, (235, 118, 318)[i], 24, fill, radius=4)
        b.text(1025, y + 29, (8, 4, 12)[i], 13, ink, 650)
    b.anchor('dashboard-metrics', 253, 138, 1157, 111)
    b.anchor('app-list', 253, 269, 721, 445)
    b.anchor('app-list-value', 279, 398, 290, 47)
    b.anchor('dashboard-chart', 991, 269, 419, 445)
    b.anchor('dashboard-config', 1200, 14, 86, 34)
    return b


def phone_grid(b):
    b.rect(0, 0, 420, 900, WHITE)
    b.text(25, 36, '9:41', 15, INK, 650)
    for i, h in enumerate((4, 6, 8, 11)):
        b.rect(326 + i * 5, 35 - h, 3, h, INK, radius=1)
    b.rect(361, 24, 28, 12, WHITE, INK, 3)
    b.rect(365, 27, 20, 6, INK, radius=2)
    b.rect(390, 28, 2, 4, INK, radius=1)
    b.text(20, 82, '‹', 27, INK, 600)
    b.text(48, 78, '项目跟进', 20, INK, 650)
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
        b.line(x, 202, x, 787)
    for x, label in ((48, '项目名称'), (216, '状态'), (295, '负责人')):
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
    b.line(0, 787, 420, 787)
    b.line(0, 821, 420, 821)
    b.text(25, 860, '数据表', 14, BLUE, 600)
    b.text(137, 860, '视图', 14, MUTED)
    b.text(229, 860, '更多', 14, MUTED)
    b.rect(150, 883, 120, 5, INK, radius=2)
    b.anchor('mobile-header', 0, 44, 420, 56)
    b.anchor('view-tabs', 0, 101, 420, 46)
    b.anchor('table-header', 0, 201, 420, 42)
    b.anchor('field-add', 369, 201, 47, 42)
    b.anchor('grid-body', 0, 243, 420, 544)
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
    for i, (label, value) in enumerate((('字段名称', '新字段'), ('字段类型', '文本'), ('默认值', '请输入默认值'))):
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
    b.anchor('default-value', 21, 678, 378, 44)
    return b


def excel_import_map():
    b = Board('excel-import-map', 'Excel 追加导入映射', ['导入映射', '数据预览', '确认导入'])
    grid(b)
    dim(b)
    b.panel(214, 103, 1012, 708, '追加导入 Excel', '把工作表数据追加到现有数据表')
    b.text(1183, 139, '×', 20, MUTED)
    for x, label, current in ((237, '1  选择文件', False), (437, '2  匹配字段', True), (637, '3  确认导入', False)):
        b.rect(x, 181, 169, 35, TINT if current else PANEL, radius=6)
        b.text(x + 16, 204, label, 14, BLUE if current else MUTED, 650 if current else 400)
    b.text(239, 259, '示例导入.xlsx', 15, INK, 650)
    b.text(416, 259, '工作表：项目跟进  ⌄', 14, MUTED)
    b.text(861, 259, '目标数据表：项目跟进  ⌄', 14, MUTED)
    b.rect(238, 281, 964, 302, WHITE, LINE, 7)
    b.rect(239, 282, 962, 43, PANEL)
    for x, label in ((258, 'Excel 列'), (552, '示例值'), (847, 'Base 字段')):
        b.text(x, 309, label, 14, MUTED, 600)
    for x in (529, 818):
        b.line(x, 282, x, 582)
    for i, label in enumerate(HEADERS[:4]):
        y = 325 + 64 * i
        b.line(238, y, 1201, y)
        b.text(258, y + 40, label, 15)
        b.text(552, y + 40, (NAMES[0], '进行中', PEOPLE[0], '2026-05-12')[i], 14, MUTED)
        b.rect(843, y + 14, 334, 36, WHITE, LINE, 5)
        b.text(856, y + 38, label, 14, INK, 550)
        b.text(1149, y + 38, '⌄', 17, MUTED)
    b.rect(238, 602, 964, 54, PANEL, LINE, 6)
    b.text(255, 635, '当前匹配 4 列。可在确认导入前检查字段与记录预览。', 14, MUTED)
    b.line(215, 730, 1225, 730)
    b.button(237, 752, '上一步', False, 94)
    b.button(1007, 752, '取消', False, 83)
    b.button(1102, 752, '下一步', True, 99)
    b.anchor('import-modal', 214, 103, 1012, 708)
    b.anchor('import-progress', 237, 181, 569, 35)
    b.anchor('import-mapping', 238, 281, 964, 302)
    b.anchor('mapping-target', 843, 339, 334, 36)
    b.anchor('import-review', 238, 602, 964, 54)
    b.anchor('import-actions', 999, 744, 210, 49)
    return b


def build(factories, render=False, renderer=None):
    boards = [factory() for factory in factories]
    for board in boards:
        board.write()
    (HERE / 'catalog.json').write_text(json.dumps(
        dict(schema_version=1, templates=[board.meta for board in boards]),
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if render:
        command = [renderer] if renderer else ['npx', '-y', '@larksuite/whiteboard-cli@0.2.13']
        def render_one(board):
            subprocess.run(command + ['-f', 'svg', '--scale', '1', '-i', str(HERE / board.meta['svg']),
                                      '-o', str(HERE / board.meta['png'])],
                           check=True, stdout=subprocess.DEVNULL)
        with ThreadPoolExecutor(max_workers=3) as workers:
            list(workers.map(render_one, boards))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true', help='Regenerate PNG previews')
    parser.add_argument('--renderer', help='Optional executable path to whiteboard-cli')
    args = parser.parse_args()
    build([
        desktop_grid, field_picker, field_config, record_detail, editor_modal,
        kanban, calendar, gantt, gallery, form, app_dashboard,
        mobile_grid, mobile_sheet, excel_import_map,
    ], args.render, args.renderer)
