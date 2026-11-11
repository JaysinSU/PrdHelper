"""Base forms, dashboard and questionnaire underlays traced from reference layouts.

The screenshots establish shell geometry and information density. All data below
is fictional. Decorative artwork is intentionally reduced to editable primitives.
"""
from base_chrome import (Board, chrome, INK, MUTED, FAINT, LINE, PANEL, BG,
                         WHITE, BLUE, TINT, WIDTH, HEIGHT, SIDEBAR)


def icon(b, x, y, name='text', color=MUTED, scale=1):
    """Small semantic line icons; no raster glyphs or flattened SVG groups."""
    s = scale
    if name == 'text':
        b.text(x, y + 12*s, 'A', 13*s, color)
        b.line(x+11*s, y+3*s, x+17*s, y+3*s, color)
        b.line(x+11*s, y+7*s, x+17*s, y+7*s, color)
        b.line(x+11*s, y+11*s, x+17*s, y+11*s, color)
    elif name == 'date':
        b.rect(x, y+2*s, 14*s, 12*s, WHITE, color, 1)
        b.line(x, y+6*s, x+14*s, y+6*s, color)
        b.line(x+4*s, y, x+4*s, y+4*s, color)
        b.line(x+10*s, y, x+10*s, y+4*s, color)
    elif name in ('select', 'radio'):
        b.circle(x+7*s, y+7*s, 6*s, WHITE)
        b.nodes.append(f'<circle cx="{x+7*s}" cy="{y+7*s}" r="{6*s}" fill="none" stroke="{color}"/>')
        b.line(x+4*s, y+6*s, x+7*s, y+9*s, color)
        b.line(x+7*s, y+9*s, x+10*s, y+6*s, color)
    elif name == 'person':
        b.nodes.append(f'<circle cx="{x+7*s}" cy="{y+4*s}" r="{3*s}" fill="none" stroke="{color}"/>')
        b.rect(x+1*s, y+9*s, 12*s, 6*s, WHITE, color, 2)
    elif name == 'check':
        b.rect(x, y+1*s, 13*s, 13*s, WHITE, color, 1)
        b.line(x+3*s, y+7*s, x+6*s, y+10*s, color)
        b.line(x+6*s, y+10*s, x+11*s, y+4*s, color)
    elif name == 'list':
        for i in range(3):
            b.line(x+5*s, y+(3+i*5)*s, x+15*s, y+(3+i*5)*s, color)
            b.circle(x+1*s, y+(3+i*5)*s, 1*s, color)
    elif name == 'file':
        b.rect(x+2*s, y, 10*s, 14*s, WHITE, color, 1)
        b.line(x+5*s, y+5*s, x+10*s, y+5*s, color)
        b.line(x+5*s, y+9*s, x+10*s, y+9*s, color)
    elif name == 'hash':
        b.text(x, y+13*s, '#', 17*s, color)
    elif name == '123':
        b.rect(x,y+2*s,16*s,11*s,WHITE,color,2)
        b.text(x+2*s,y+10*s,'123',6*s,color)
    elif name == '▰':
        b.rect(x,y+4*s,16*s,7*s,WHITE,color,3)
        for dx in (4,7,10): b.line(x+dx*s,y+5*s,x+(dx-2)*s,y+10*s,color)
    elif name == '⌖':
        b.circle(x+7*s,y+5*s,4*s,'none',color)
        b.circle(x+7*s,y+5*s,1*s,color)
        b.line(x+3*s,y+8*s,x+7*s,y+14*s,color)
        b.line(x+7*s,y+14*s,x+11*s,y+8*s,color)
    else:
        b.text(x, y+13*s, name, 14*s, color)


def small_action(b, x, y, label, w, active=False):
    b.rect(x, y, w, 26, TINT if active else WHITE, LINE, 4)
    b.text(x+10, y+18, label, 12, BLUE if active else INK)


def toggle(b, x, y, on=False):
    b.rect(x, y, 24, 13, BLUE if on else '#c8cdd3', radius=6)
    b.circle(x+17 if on else x+7, y+6.5, 5, WHITE)


def chevron(b, x, y, color=MUTED):
    b.line(x,y,x+4,y+4,color)
    b.line(x+4,y+4,x+8,y,color)


def cover(b, x, y, w, h, editable=False):
    b.rect(x, y, w, h, '#e9eef6')
    # Keep the cover's size and abstract rhythm without copying bitmap artwork.
    for cx, cy, r in ((x+70, y+118, 15), (x+w*.34, y+55, 20),
                      (x+w*.70, y+60, 21), (x+w*.94, y+81, 10)):
        b.circle(cx, cy, r, '#d8e2ef')
    for xx, yy in ((x+116, y+78), (x+w*.46, y+14), (x+w*.80, y+95)):
        b.rect(xx, yy, 75, 24, '#d3ddeb', radius=12)
    if editable:
        small_action(b, x+w-84, y+14, '编辑封面', 70)


def form_toolbar(b, editing=False):
    b.rect(SIDEBAR, 96, WIDTH-SIDEBAR, 41, WHITE)
    b.line(SIDEBAR, 137, WIDTH, 137)
    # Segmented switch remains centered in the content region in both states.
    x = 833
    b.rect(x, 101, 166, 28, WHITE, LINE, 4)
    b.rect(x+3 if editing else x+84, 104, 79, 22, TINT, radius=3)
    b.text(x+10, 120, '编辑表单', 12, BLUE if editing else INK)
    b.text(x+93, 120, '填写表单', 12, INK if editing else BLUE)
    small_action(b, 1434 if editing else 1490, 102, '分享表单', 76)
    if editing:
        b.text(1527, 120, '⚙', 16, MUTED)
        b.icon('more',1564,108,13)


def form_card(b, x, y, w=494, editing=False):
    b.rect(x, y, w, HEIGHT-y, WHITE, LINE, 9)
    b.text(x+w/2-22, y+65, '表单', 23, INK, 650)
    innerx, inputw = x+40, w-80
    if editing:
        b.text(innerx, y+104, '请输入表单描述', 12, FAINT)
        first, step = y+156, 87
    else:
        first, step = y+112, 86
    fields = [('门店编号', '请输入内容', 'text'),
              ('门店名称', '请输入内容', 'text'),
              ('门店类型', '请选择选项', 'select'),
              ('所属区域', '请选择选项', 'select'),
              ('城市', '请输入内容', 'text'),
              ('门店负责人', '请选择人员', 'select')]
    for i,(label, placeholder, kind) in enumerate(fields):
        yy = first+i*step
        if yy+50 > HEIGHT-8:
            break
        if editing:
            for dx in (0, 4):
                for dy in (0, 4, 8):
                    b.circle(x+18+dx, yy-6+dy, .7, FAINT)
            toggle(b, x+w-126, yy-9)
            b.text(x+w-97, yy+1, '必填', 12, MUTED)
            b.nodes.append(f'<circle cx="{x+w-53}" cy="{yy-3}" r="6" fill="none" stroke="{FAINT}"/>')
            b.line(x+w-56, yy-3, x+w-50, yy-3, FAINT)
        b.text(innerx, yy, label, 12, INK)
        if i == 0 and editing:
            b.icon('lock', innerx+56, yy-12, 11, FAINT)
        b.rect(innerx, yy+13, inputw, 28, WHITE, LINE, 4)
        b.text(innerx+8, yy+31, '填写者回答区' if editing else placeholder, 12, FAINT)
        if kind == 'select':
            b.line(innerx+inputw-17, yy+25, innerx+inputw-13, yy+29, MUTED)
            b.line(innerx+inputw-13, yy+29, innerx+inputw-9, yy+25, MUTED)
    if not editing:
        b.text(innerx, 855, '区域经理', 12, INK)
        b.text(innerx, 877, '字段描述：填写对应的负责人信息。', 11, MUTED)
        b.text(innerx, 896, '信息仅用于业务协作与记录。', 11, MUTED)
    b.anchor('form-card', x, y, w, HEIGHT-y)
    b.anchor('form-title', x+40, y+25, w-80, 55)
    b.anchor('form-first-field', innerx, first-15, inputw, 58)


def form_edit():
    b = Board('form-edit', '表单视图（编辑态）', ['配置题目与必填状态', '添加或移除题目'])
    chrome(b, active='表单', toolbar=False)
    form_toolbar(b, True)
    b.rect(SIDEBAR, 137, 240, HEIGHT-137, WHITE)
    b.line(444, 137, 444, HEIGHT)
    b.text(218, 167, '可选题目', 12, INK, 600)
    b.text(330, 167, '全部添加', 10, BLUE)
    b.text(385, 167, '全部移除', 10, BLUE)
    for i, label in enumerate(('备注', '补充说明')):
        icon(b, 224, 188+31*i, 'text')
        b.text(246, 200+31*i, label, 12, INK)
        b.text(411, 202+31*i, '+', 20, FAINT)
    b.line(218, 241, 430, 241)
    b.text(218, 267, '新增题目', 12, INK, 600)
    sections = [
        (300, '基础题型', [('文本','text'),('单选','select'),('多选','list'),('日期','date'),('附件','file'),('数字','hash'),('人员','person')]),
        (478, '常用题型', [('评分','☆'),('NPS','123'),('进度','▰'),('复选框','check'),('超链接','↗'),('电话号码','☎'),('Email','✉'),('地理位置','⌖'),('条码','▥'),('货币','¥'),('群组','person'),('明细表','list')]),
        (722, '高级题型', [('双向关联','↔'),('单向关联','↗'),('公式','ƒ'),('查找引用','file')])]
    for yy, heading, opts in sections:
        b.text(218, yy, heading, 11, MUTED)
        for i,(label,kind) in enumerate(opts):
            xx = 218+(i%2)*109
            sy = yy+13+(i//2)*34
            b.rect(xx, sy, 102, 27, '#f1f3f5', radius=4)
            icon(b, xx+7, sy+5, kind)
            b.text(xx+28, sy+18, label, 11, INK)
    cover(b, 444, 137, WIDTH-444, 171, True)
    form_card(b, 768, 232, editing=True)
    b.anchor('question-palette', 204, 137, 240, 787)
    b.anchor('cover', 444, 137, 1156, 171)
    b.anchor('form-mode-switch', 833, 101, 166, 28)
    return b


def form_fill():
    b = Board('form-fill', '表单视图（填写态）', ['填写已有表单', '查看题目描述和选项'])
    chrome(b, active='表单', toolbar=False)
    form_toolbar(b, False)
    cover(b, SIDEBAR, 137, WIDTH-SIDEBAR, 171)
    form_card(b, 651, 232)
    b.anchor('cover', 204, 137, 1396, 171)
    b.anchor('form-mode-switch', 833, 101, 166, 28)
    return b


def dashboard():
    b = Board('dashboard', '仪表盘', ['图表组件', '数据筛选', '明细表组件与布局适配'])
    chrome(b, mode='dashboard', selected='库存与损耗数据分析', toolbar=False)
    b.rect(SIDEBAR, 56, WIDTH-SIDEBAR, HEIGHT-56, '#f2f3f5')
    b.icon('chart',229,72,13)
    b.text(251, 84, '订货与库存分析仪表盘', 13, INK, 600)
    for x,w,label in ((439,79,'＋ 添加组件'),(524,53,'筛选'),(584,118,'设置自动化发送'),(709,55,'主题')):
        small_action(b, x, 68, label, w)
    for x,w,label in ((1170,78,'智能总结'),(1254,78,'订阅数据'),(1338,90,'生成页面'),(1435,93,'已开启分享')):
        small_action(b, x, 68, label, w)
    b.icon('more',1550,74,13)
    # Full-width filter strip, two KPI cards, three chart cards, then detail table.
    b.rect(224, 106, 1356, 75, WHITE, radius=13)
    b.text(241, 150, '门店筛选器', 14, INK, 600)
    b.text(326, 150, '请选择', 14, FAINT)
    chevron(b,1542,143)
    for x,title,value in ((224,'近期订货总数量','163'),(910,'近期实盘库存总量','109')):
        b.rect(x, 196, 670, 164, WHITE, radius=13)
        b.text(x+40, 251, title, 16, MUTED)
        b.text(x+40, 312, value, 58, INK, 650)
    chart_y, chart_h = 373, 389
    for x,w,title in ((224,444,'损耗原因分布'),(682,444,'缺货等级分布'),(1140,440,'各门店订货数量排行')):
        b.rect(x, chart_y, w, chart_h, WHITE, radius=13)
        b.text(x+18, chart_y+31, title, 14, INK, 600)
    # Editable pie outline, radial separators and labels.
    for x,label,fill in ((241,'过期','#c6d5f1'),(285,'制作损耗','#d4e8e3'),(363,'盘点误差','#eee5cb'),(441,'空值','#e2d3ce')):
        b.circle(x, 423, 3.4, fill)
        b.text(x+8, 427, label, 10, MUTED)
    cx,cy,r = 447,591,91
    b.nodes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f3f5f8" stroke="{LINE}"/>')
    for px,py in ((447,500),(533,562),(447,682),(392,664)):
        b.line(cx,cy,px,py,FAINT)
    b.line(533,562,552,562,FAINT)
    b.text(557,566,'过期：2（20%）',10,MUTED)
    b.line(447,682,488,697,FAINT)
    b.text(493,703,'制作损耗：3',10,MUTED)
    b.line(392,664,315,686,FAINT)
    b.text(242,700,'盘点误差：1',10,MUTED)
    b.line(356,591,326,591,FAINT)
    b.text(241,591,'空值：4（40%）',10,MUTED)
    # Simple bar chart matches two-category visualization and axis density.
    b.circle(701,423,3.4,'#9fadc2'); b.text(711,427,'计数',10,MUTED)
    for i,val in enumerate((0,2,4,6,8)):
        yy=720-i*67
        b.line(721,yy,1108,yy,LINE)
        b.text(699,yy+4,val,10,FAINT)
    b.rect(766,687,45,33,'#ccd8ec',radius=4)
    b.rect(1016,486,45,234,'#ccd8ec',radius=4)
    b.text(784,709,'1',11,MUTED); b.text(1034,507,'7',11,MUTED)
    b.text(784,742,'低',11,MUTED); b.text(1034,742,'高',11,MUTED)
    # Ranking places top 1 in the middle as in the source.
    for cx,yy,rank,label,val in ((1222,472,'2','示例门店 B','40'),(1359,449,'1','示例门店 A','60'),(1496,472,'3','示例门店 C','35')):
        b.circle(cx,yy,20,'#edf0f4')
        b.nodes.append(f'<circle cx="{cx}" cy="{yy}" r="14" fill="none" stroke="{FAINT}"/>')
        b.text(cx-5,yy+6,rank,18,MUTED,650)
        b.line(cx-9,yy+18,cx-9,yy+29,FAINT,3)
        b.line(cx+9,yy+18,cx+9,yy+29,FAINT,3)
        b.text(cx-35,yy+45,label,10,MUTED)
        b.text(cx-10,yy+64,val,17,INK,600)
    b.rect(1157,552,404,103,'#f5f6f8',LINE,7)
    for i,(name,val) in enumerate((('示例门店 D','28'),('示例门店 E','0'),('示例门店 F','0'))):
        yy=574+34*i
        b.text(1171,yy,i+4,10,MUTED); b.text(1195,yy,name,10,MUTED)
        b.text(1536,yy,val,10,MUTED)
    b.rect(224,775,1356,149,WHITE,radius=13)
    b.text(241,806,'近期订货库存与损耗明细',14,INK,600)
    xs=[241,556,633,710,787,864]
    b.rect(241,826,623,27,'#edf1f8',LINE,6)
    for i,(label,x) in enumerate(zip(('门店名','订货','盘点','损耗','总计'),xs)):
        b.text(x+8,845,label,11,INK,600)
    for i in range(2):
        yy=853+i*28
        b.line(241,yy+28,864,yy+28,LINE)
        b.text(249,yy+19,f'示例门店 {chr(65+i)}',11,MUTED)
        for j in range(1,5): b.text(xs[j]+31,yy+19,1 if j==4 else '—',11,MUTED)
    for xx in xs: b.line(xx,826,xx,909,LINE)
    b.anchor('dashboard-toolbar',204,56,1396,50)
    b.anchor('dashboard-filter',224,106,1356,75)
    b.anchor('metric-cards',224,196,1356,164)
    b.anchor('chart-cards',224,373,1356,389)
    b.anchor('detail-table',224,775,1356,149)
    return b


def survey_tabs(b, active='收集表'):
    # Replace the view tabs; surveys have a dedicated collection/results switch.
    b.rect(SIDEBAR,56,WIDTH-SIDEBAR,40,'#f4f5f6')
    for x,label,w in ((216,'收集表',89),(310,'收集结果',101)):
        if label==active: b.rect(x,57,w,39,WHITE,radius=7)
        b.icon('form' if label=='收集表' else 'table',x+10,69,12,BLUE if active==label else MUTED)
        b.text(x+30,82,label,13,INK if active==label else MUTED)
    b.text(424,82,'+',20,MUTED)
    b.anchor('collection-tabs',204,56,1396,40)


def questionnaire():
    b = Board('questionnaire','问卷',['配置收集表题目','长内容题型与预览'])
    chrome(b, mode='dashboard', selected='收集表 4', toolbar=False)
    survey_tabs(b)
    b.rect(SIDEBAR,96,WIDTH-SIDEBAR,48,WHITE)
    for x,label in ((1250,'样式'),(1284,'设置'),(1318,'预览'),(1352,'评论'),(1386,'嵌入'),(1420,'展开')):
        b.circle(x+10,118,12,WHITE)
        b.nodes.append(f'<circle cx="{x+10}" cy="118" r="12" fill="none" stroke="{LINE}"/>')
        if label=='样式':
            b.circle(x+10,118,6,'none',MUTED)
            for dx,dy in ((-2,-2),(3,-2),(-2,3)): b.circle(x+10+dx,118+dy,1,MUTED)
        elif label=='设置': b.text(x+4,122,'⚙',12,MUTED)
        elif label=='预览':
            b.nodes.append(f'<ellipse cx="{x+10}" cy="118" rx="7" ry="4" fill="none" stroke="{MUTED}"/>')
            b.circle(x+10,118,2,MUTED)
        elif label=='评论':
            b.rect(x+4,113,12,8,'none',MUTED,2)
            b.line(x+6,121,x+6,124,MUTED);b.line(x+6,124,x+9,121,MUTED)
        elif label=='嵌入':
            b.rect(x+4,112,12,12,'none',MUTED,1)
            b.line(x+4,116,x+16,116,MUTED)
            b.line(x+7,119,x+13,119,MUTED)
        else:
            b.line(x+5,122,x+14,113,MUTED)
            b.line(x+10,113,x+14,113,MUTED)
            b.line(x+14,113,x+14,117,MUTED)
    small_action(b,1454,106,'结果分析',66)
    b.button(1531,106,'发布',True,w=55,h=26)
    # A full canvas with a broad single-column question flow and right artwork.
    b.rect(218,144,1368,780,'#f2f7f9',radius=10)
    b.text(357,235,'收集表',27,'#526b7b',650)
    b.text(357,271,'请输入描述',14,'#94a6b1')
    b.text(323,330,'*1→',12,MUTED)
    b.text(357,331,'文本',16,'#526b7b',600)
    b.text(357,352,'问题描述',12,'#94a6b1')
    b.rect(357,372,592,69,'none','#b8c9d3',5)
    b.text(369,396,'待填写者输入',14,'#94a6b1')
    b.text(329,514,'2→',12,MUTED)
    b.text(357,515,'查找引用',16,'#526b7b',600)
    b.nodes.append('<circle cx="431" cy="508" r="6" fill="none" stroke="#94a6b1"/>')
    b.text(429,512,'i',10,'#94a6b1')
    b.text(357,536,'问题描述',12,'#94a6b1')
    b.rect(357,555,592,34,'#e7eef2',radius=5)
    b.text(369,578,'[门店信息表].[门店名称]',14,'#94a6b1')
    b.text(323,664,'*3→',12,MUTED)
    b.text(357,665,'多选题',16,'#526b7b',600)
    b.text(357,686,'问题描述',12,'#94a6b1')
    for i in range(3):
        yy=705+i*41
        b.rect(357,yy,592,34,'none','#b8c9d3',6)
        b.nodes.append(f'<circle cx="379" cy="{yy+17}" r="6" fill="none" stroke="#94a6b1"/>')
        b.text(393,yy+22,i+1,12,'#7e929e')
    b.text(329,901,'4→',12,MUTED)
    b.text(357,902,'文件上传',16,'#526b7b',600)
    # Editable line-art placeholder for the original right-hand decorative vase.
    b.nodes.append('<ellipse cx="1325" cy="808" rx="103" ry="97" fill="#edf3f6" stroke="#dce6ec"/>')
    b.rect(1262,662,126,102,'#edf3f6','#dce6ec',8)
    b.line(1325,819,1280,478,'#cedbd4',3)
    b.nodes.append('<ellipse cx="1267" cy="422" rx="24" ry="44" fill="#edf1eb" stroke="#d9e4dd"/>')
    b.nodes.append('<ellipse cx="1294" cy="424" rx="23" ry="43" fill="#edf1eb" stroke="#d9e4dd"/>')
    b.nodes.append('<ellipse cx="1308" cy="567" rx="14" ry="30" fill="#edf1eb" stroke="#d9e4dd"/>')
    b.nodes.append('<ellipse cx="1284" cy="618" rx="20" ry="11" fill="#edf1eb" stroke="#d9e4dd"/>')
    b.rect(1399,368,120,527,'#eef4f7','#e2ebef',12)
    b.anchor('survey-toolbar',204,96,1396,48)
    b.anchor('survey-canvas',218,144,1368,780)
    b.anchor('question-flow',323,305,626,516)
    b.anchor('first-answer',357,372,592,69)
    b.anchor('lookup-answer',357,555,592,34)
    return b


def questionnaire_results():
    b = Board('questionnaire-results','问卷关联数据表',['收集结果与数据表字段映射','数据消费与字段展示'])
    chrome(b, mode='dashboard', selected='收集表 4', toolbar=False)
    survey_tabs(b,'收集结果')
    b.rect(SIDEBAR,96,WIDTH-SIDEBAR,32,WHITE)
    b.line(SIDEBAR,128,WIDTH,128,LINE)
    b.text(225,118,'＋ 添加记录',13,BLUE)
    for xx,label,kind in ((323,'字段配置','table'),(410,'视图配置','table'),(496,'筛选','filter'),(554,'分组','gallery'),(613,'排序','text'),(670,'行高','text'),(729,'填色','chart')):
        b.icon(kind,xx,106,11)
        b.text(xx+17,118,label,12,MUTED)
    b.text(1272,118,'智能提醒',11,FAINT)
    b.text(1352,118,'生成页面',11,FAINT)
    for xx,direction in ((1487,-1),(1523,1)):
        b.line(xx,116,xx+12,116,MUTED)
        b.line(xx+12,116,xx+12,109,MUTED)
        b.line(xx+12,109,xx+2,109,MUTED)
        if direction==-1:
            b.line(xx+2,109,xx+6,105,MUTED); b.line(xx+2,109,xx+6,113,MUTED)
        else:
            b.line(xx+12,109,xx+8,105,MUTED); b.line(xx+12,109,xx+8,113,MUTED)
    b.icon('search',1562,107,12)
    xs=[204,250,493,647,800,955,1108,1263,1418,1600]
    labels=[('自动编号','list'),('文本','text'),('多选题','select'),('提交时间','date'),('提交人','person'),('文件上传','file'),('查找引用','file'),('NPS 净推荐值','☆')]
    b.rect(204,128,1396,30,'#fbfcfd')
    b.rect(227,138,11,11,WHITE,FAINT,1)
    for i,(label,kind) in enumerate(labels):
        icon(b,xs[i+1]+10,137,kind)
        b.text(xs[i+1]+31,149,label,12,INK)
    for yy in (128,158,186,214,242,270): b.line(204,yy,1600,yy,LINE)
    for xx in xs: b.line(xx,128,xx,242,LINE)
    texts=['','今天补充最新门店信息…','需要核实使用场景…']
    for i in range(3):
        yy=158+i*28
        b.text(228,yy+19,i+1,11,FAINT)
        b.text(261,yy+19,i+1,12,INK)
        b.text(501,yy+19,texts[i],12,INK)
        if i:
            b.pill(655,yy+5,'1',fill='#e5ecfb',ink='#536b9c',w=19)
        b.text(809,yy+19,'2026/08/13',12,INK)
        b.circle(974,yy+14,8,'#e1e9ee')
        b.text(988,yy+19,'成员 A',12,INK)
        for j in range(10):
            xx=1427+j*16
            b.rect(xx,yy+7,12,12,'#e5e7eb',radius=2)
            b.text(xx+3,yy+16,j,7,WHITE)
    b.text(226,264,'+',20,FAINT)
    b.line(204,896,1600,896,LINE)
    b.text(293,914,'3 条记录',10,MUTED)
    chevron(b,341,907)
    b.anchor('results-toolbar',204,96,1396,32)
    b.anchor('results-header',204,128,1396,30)
    b.anchor('results-grid',204,158,1396,84)
    b.anchor('result-text-field',493,128,154,114)
    b.anchor('result-lookup-field',1263,128,155,114)
    return b


def build_all():
    return [form_edit(), form_fill(), dashboard(), questionnaire(), questionnaire_results()]


if __name__ == '__main__':
    for board in build_all():
        board.write()
