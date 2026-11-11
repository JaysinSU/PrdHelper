#!/usr/bin/env python3
"""Base workflow and advanced permissions shells, redrawn from supplied references."""
from base_chrome import (Board, chrome, INK, MUTED, FAINT, LINE, PANEL, BG,
                         WHITE, BLUE, TINT, WIDTH, HEIGHT, SIDEBAR)


def ellipsis(b, x, y, color=MUTED):
    for dx in (-5, 0, 5):
        b.circle(x + dx, y, 1.2, color)


def toggle(b, x, y, enabled=False):
    b.rect(x, y, 34, 18, BLUE if enabled else '#cbd0d6', radius=9)
    b.circle(x + (25 if enabled else 9), y + 9, 7, WHITE)


def chevron(b, x, y, direction='down', color=MUTED):
    if direction == 'down':
        b.line(x - 4, y - 2, x, y + 2, color, 1.3)
        b.line(x, y + 2, x + 4, y - 2, color, 1.3)
    else:
        b.line(x - 3, y - 4, x + 2, y, color, 1.3)
        b.line(x + 2, y, x - 3, y + 4, color, 1.3)


def table_icon(b, x, y, color=MUTED):
    b.rect(x, y, 10, 11, WHITE, color, 1)
    b.line(x + 2, y + 3, x + 8, y + 3, color, .8)
    b.line(x + 2, y + 6, x + 8, y + 6, color, .8)
    b.line(x + 4, y + 3, x + 4, y + 9, color, .8)


def person_icon(b, x, y, color=MUTED):
    b.circle(x, y - 4, 3, WHITE)
    b.nodes.append(f'<circle cx="{x}" cy="{y - 4}" r="3" fill="none" stroke="{color}" stroke-width="1.2"/>')
    b.rect(x - 5, y + 1, 10, 5, WHITE, color, 2)


def pencil_icon(b, x, y, color=WHITE):
    b.line(x - 4, y + 4, x + 5, y - 5, color, 3)
    b.line(x - 6, y + 7, x - 4, y + 4, color, 1.4)
    b.line(x - 6, y + 7, x - 2, y + 6, color, 1.4)
    b.line(x - 6, y + 10, x + 7, y + 10, color, 1.2)


def draw_workflow_canvas(b):
    b.rect(SIDEBAR, 56, WIDTH - SIDEBAR, HEIGHT - 56, '#f5f6f8')
    # Workflow mark: one parent node and two child branches.
    b.rect(222, 72, 5, 5, 'none', MUTED, 1)
    b.rect(218, 81, 5, 5, 'none', MUTED, 1)
    b.rect(227, 81, 5, 5, 'none', MUTED, 1)
    b.line(225, 77, 225, 80, MUTED, 1)
    b.line(220, 80, 230, 80, MUTED, 1)
    b.text(237, 83, '工作流1', 14, INK, 550)
    b.line(463, 72, 463, 84, LINE)
    toggle(b, 481, 71)
    b.text(1421, 84, '运行日志', 13, MUTED)
    b.line(1407, 80, 1412, 75, MUTED, 1.3)
    b.line(1412, 75, 1417, 78, MUTED, 1.3)
    b.button(1501, 65, '保存并启用', True, 84, 28)

    x, w, h, cx = 730, 345, 74, 902
    b.line(cx, 407, cx, 476, '#c4c9cf', 1.2)
    b.line(cx, 550, cx, 616, '#c4c9cf', 1.2)
    for y, index, title, description in (
        (334, '1', '修改记录时', '数据表：数据表1'),
        (476, '2', '发送飞书消息', '接收方：示例成员'),
    ):
        b.text(710, y + 42, index, 13, FAINT)
        b.rect(x, y, w, h, WHITE, '#e7e9ed', 12)
        if index == '1':
            b.rect(x + 18, y + 18, 38, 38, '#df59ae', radius=8)
            pencil_icon(b, x + 37, y + 34)
        else:
            b.rect(x + 18, y + 18, 38, 38, WHITE, LINE, 8)
            b.circle(x + 36, y + 36, 7, '#3976ef')
            b.rect(x + 30, y + 39, 7, 3, '#3976ef')
            b.circle(x + 42, y + 40, 5, '#34c4bd')
        b.text(x + 67, y + 32, title, 15, INK, 550)
        b.text(x + 67, y + 51, description, 13, MUTED)
    b.circle(cx, 334, 13, WHITE)
    b.line(cx + 2, 326, cx - 3, 335, INK, 2)
    b.line(cx - 3, 335, cx + 4, 333, INK, 2)
    b.line(cx + 4, 333, cx - 1, 342, INK, 2)
    b.rect(cx - 13, 618, 26, 26, WHITE, '#bfc5ce', 4)
    b.line(cx - 6, 631, cx + 6, 631, MUTED, 1.3)
    b.line(cx, 625, cx, 637, MUTED, 1.3)

    # Canvas controls match the bottom-right placement in the reference.
    b.text(1374, 872, '100%', 11, FAINT)
    for px in (1357, 1412):
        b.nodes.append(f'<circle cx="{px}" cy="867" r="6" fill="none" stroke="{FAINT}" stroke-width="1.1"/>')
        b.line(px - 3, 867, px + 3, 867, FAINT, 1)
    b.line(1412, 864, 1412, 870, FAINT, 1)
    for px in (1439, 1467):
        b.rect(px - 5, 862, 10, 10, 'none', FAINT, 1)
    b.line(1324, 860, 1324, 872, FAINT, 1)
    b.line(1319, 865, 1329, 865, FAINT, 1)
    b.anchor('workflow-header', SIDEBAR, 56, WIDTH - SIDEBAR, 46)
    b.anchor('workflow-state', 480, 70, 36, 20)
    b.anchor('workflow-canvas', SIDEBAR, 103, WIDTH - SIDEBAR, HEIGHT - 103)
    b.anchor('workflow-trigger', x, 334, w, h)
    b.anchor('workflow-action', x, 476, w, h)
    b.anchor('workflow-add-step', cx - 13, 618, 26, 26)
    b.anchor('workflow-save', 1501, 65, 84, 28)


def workflow():
    b = Board('workflow', '工作流', ['触发器、动作节点与添加步骤', '保存并启用工作流'])
    chrome(b, mode='workflow', selected='工作流1', toolbar=False)
    draw_workflow_canvas(b)
    return b


def advanced_permissions():
    b = Board('advanced-permissions', '高级权限', ['角色权限', '数据表访问范围', '权限配置与保存'])
    chrome(b, mode='workflow', selected='工作流1', toolbar=False)
    draw_workflow_canvas(b)
    b.nodes.append('<rect x="0" y="0" width="1600" height="924" fill="#000000" opacity="0.49"/>')
    mx, my, mw, mh = 124, 43, 1352, 881
    b.rect(mx, my, mw, mh, WHITE, radius=13)
    b.line(mx, 94, mx + mw, 94)
    # Title mark is a small locked data panel, not an empty placeholder box.
    b.rect(148, 62, 14, 13, BLUE, radius=2)
    b.line(151, 66, 159, 66, WHITE, 1)
    b.line(151, 69, 157, 69, WHITE, 1)
    b.circle(161, 75, 4, WHITE)
    b.rect(159, 74, 4, 4, BLUE, radius=1)
    b.text(172, 74, '高级权限', 16, INK, 650)
    toggle(b, 256, 60, True)
    b.line(305, 62, 305, 76, LINE)
    b.text(319, 74, '允许通过分享授权', 13, INK)
    chevron(b, 429, 69)
    b.text(1354, 74, '问问 AI', 13, MUTED)
    b.line(1418, 60, 1418, 78, LINE)
    b.line(1441, 63, 1452, 74, MUTED, 1.5)
    b.line(1441, 74, 1452, 63, MUTED, 1.5)
    # Left role navigation.
    b.line(353, 94, 353, 924)
    b.text(155, 131, '系统角色', 11, FAINT)
    for i, label in enumerate(('所有者', '管理员', '编辑者', '阅读者')):
        y = 157 + i * 34
        active = label == '编辑者'
        if active:
            b.rect(145, y - 17, 188, 33, '#e7eeff', radius=6)
        if label == '编辑者':
            pencil_icon(b, 164, y - 2, BLUE)
        elif label == '阅读者':
            b.nodes.append(f'<ellipse cx="164" cy="{y - 1}" rx="6" ry="4" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
            b.circle(164, y - 1, 1.5, MUTED)
        else:
            person_icon(b, 164, y - 1)
        b.text(177, y + 4, label, 14, BLUE if active else INK, 550 if active else 400)
    b.line(145, 286, 333, 286)
    b.text(155, 314, '自定义角色', 11, FAINT)
    b.circle(219, 310, 4, WHITE)
    b.text(217, 313, 'i', 9, FAINT)
    person_icon(b, 164, 339)
    b.text(177, 343, '普通用户', 14, INK)
    b.text(155, 378, '+', 20, BLUE)
    b.text(176, 376, '添加角色', 14, BLUE)
    b.line(145, 400, 333, 400)
    b.line(156, 425, 161, 417, MUTED, 1.2)
    b.line(161, 417, 167, 425, MUTED, 1.2)
    b.line(167, 425, 161, 432, MUTED, 1.2)
    b.line(161, 432, 156, 425, MUTED, 1.2)
    b.text(177, 430, '通过 AI 配置', 13, INK)
    b.text(176, 895, '帮助中心', 12, MUTED)
    b.circle(162, 890, 5, WHITE)
    b.text(159, 894, '?', 10, MUTED)
    # Main role title and horizontal permission tabs.
    b.text(374, 145, '编辑者', 18, INK, 650)
    for x, label in ((374, '数据权限'), (445, '仪表盘权限'), (529, '页面权限'),
                     (600, '自动化权限'), (684, '其他功能权限')):
        b.text(x, 192, label, 13, BLUE if label == '数据权限' else MUTED)
    b.line(373, 205, 1455, 205)
    b.line(374, 205, 422, 205, BLUE, 2)
    for px, fill in ((1344, TINT), (1376, '#d1e4ec'), (1408, '#8abf00'), (1440, PANEL)):
        b.circle(px, 137, 13, fill)
        if px == 1440:
            pencil_icon(b, px, 134, MUTED)
        else:
            person_icon(b, px, 137, BLUE if px == 1344 else WHITE)
    # Search and data table list in the middle column.
    b.rect(374, 226, 232, 28, WHITE, '#d1d7df', 5)
    b.nodes.append(f'<circle cx="389" cy="239" r="4" fill="none" stroke="{FAINT}" stroke-width="1.1"/>')
    b.line(392, 242, 395, 246, FAINT, 1)
    b.text(404, 244, '搜索数据表', 13, FAINT)
    chevron(b, 388, 284)
    b.text(405, 289, '文件夹', 13, INK)
    table_names = [f'数据表{i}' for i in range(1, 4)]
    for i, label in enumerate(table_names):
        y = 318 + 34 * i
        nested = True
        if i == 0:
            b.rect(374, y - 15, 232, 31, '#e7eeff', radius=6)
        table_icon(b, 400 if nested else 382, y - 7)
        b.text(417 if nested else 399, y + 3, label, 12.5, INK)
        level = ('无权限', '可编辑', '可管理')[i]
        b.text(565, y + 3, level, 10.5, FAINT)
    # Right permission card matches the read/manage/edit/no-access radio stack.
    b.rect(626, 226, 829, 168, WHITE, '#e4e7ec', 7)
    table_icon(b, 644, 242)
    b.text(662, 251, '数据表权限', 13, INK)
    b.text(1384, 251, '无权限', 11, FAINT)
    chevron(b, 1431, 247, 'right', FAINT)
    b.line(642, 268, 1438, 268)
    for i, label in enumerate(('可管理', '可编辑', '仅可阅读', '无权限')):
        y = 292 + i * 26
        selected = label == '无权限'
        b.nodes.append(f'<circle cx="650" cy="{y}" r="6" fill="{BLUE if selected else WHITE}" stroke="{BLUE if selected else "#a8b0bc"}" stroke-width="1.1"/>')
        if selected:
            b.circle(650, y, 2, WHITE)
        b.text(664, y + 4, label, 13, INK)
    b.line(353, 855, 1475, 855)
    b.button(1296, 877, '保存并预览', False, 81, 28)
    b.button(1386, 877, '保存', True, 69, 28)
    b.anchor('permission-modal', mx, my, mw, mh)
    b.anchor('permission-toggle', 256, 60, 34, 18)
    b.anchor('permission-roles', 145, 112, 188, 321)
    b.anchor('permission-tabs', 374, 173, 424, 33)
    b.anchor('permission-table-list', 374, 226, 232, 180)
    b.anchor('permission-options', 626, 226, 829, 168)
    b.anchor('permission-save', 1296, 877, 159, 28)
    return b


def build_all():
    return [workflow(), advanced_permissions()]


if __name__ == '__main__':
    for board in build_all():
        board.write()
