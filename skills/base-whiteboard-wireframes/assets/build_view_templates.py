#!/usr/bin/env python3
"""Screenshot-aligned Base table, kanban, calendar, gantt and gallery templates."""
from base_chrome import (Board, chrome, WIDTH, HEIGHT, SIDEBAR, INK, MUTED,
                         FAINT, LINE, PANEL, BG, WHITE, BLUE, TINT)

GROUPS = [('分组1','#fbefc7'),('分组2','#d9f2ed'),('分组3','#eee7fb')]
COLS = [204,250,510,710,950,1170,1600]


def compact_pill(b,x,y,label,fill=TINT,ink=INK,w=None,h=17,size=11):
    w = w or max(35,len(label)*size+12)
    b.rect(x,y,w,h,fill,radius=7)
    b.text(x+6,y+h-4,label,size,ink)


def text_icon(b,x,y,color=MUTED):
    b.text(x,y+11,'A',12,color)
    for dy in (2,6,10):
        b.line(x+10,y+dy,x+15,y+dy,color,.8)


def choice_icon(b,x,y):
    b.circle(x+5,y+5,5,WHITE)
    b.rect(x,y,10,10,'none',MUTED,5,.8)
    b.line(x+2,y+4,x+5,y+7,MUTED,.8)
    b.line(x+5,y+7,x+8,y+3,MUTED,.8)


def field_label(b,x,y,label,kind='text',size=11.5):
    if kind=='text': text_icon(b,x,y-10)
    elif kind=='choice': choice_icon(b,x,y-10)
    elif kind=='number': b.text(x,y,'#',14,MUTED)
    elif kind=='person':
        b.rect(x,y-3,10,6,'none',MUTED,2,.8)
        b.rect(x+3,y-11,4,4,'none',MUTED,3,.8)
    elif kind=='check':
        b.rect(x,y-10,10,10,'none',MUTED,1,.8)
        b.line(x+2,y-5,x+4,y-2,MUTED,.8)
        b.line(x+4,y-2,x+8,y-8,MUTED,.8)
    elif kind=='date':
        b.rect(x,y-10,11,10,'none',MUTED,1,.8)
        b.line(x,y-7,x+11,y-7,MUTED,.8)
    elif kind=='formula': b.text(x,y,'ƒ',14,MUTED)
    elif kind=='link':
        b.rect(x,y-10,7,7,'none',MUTED,2,.8)
        b.rect(x+5,y-6,7,7,'none',MUTED,2,.8)
        b.line(x+4,y-6,x+8,y-3,MUTED,.8)
    else: b.rect(x,y-10,10,10,'none',MUTED,2,.8)
    b.text(x+17,y,label,size,MUTED)


def grid_content(b, selected=False):
    # Three representative records are enough for the background table.
    y0, hh, rh = 128, 30, 32
    rows = 3
    ybottom = y0 + hh + rows * rh
    b.rect(SIDEBAR, y0, WIDTH-SIDEBAR, hh, PANEL)
    for x in COLS:
        b.line(x, y0, x, ybottom)
    b.line(SIDEBAR, y0, WIDTH, y0)
    for i in range(rows+1):
        b.line(SIDEBAR, y0+hh+i*rh, WIDTH, y0+hh+i*rh)
    b.rect(227,139,11,11,'none',MUTED,1)
    headers = [('文本1','text'),('单选1','choice'),('人员1','person'),('日期1','date'),('文本2','text')]
    for i,(label,kind) in enumerate(headers):
        field_label(b,COLS[i+1]+10,148,label,kind,11.5)
    for i in range(rows):
        y=y0+hh+i*rh
        b.text(229,y+21,i+1,11,FAINT)
        b.text(260,y+21,'示例数据',11.5,INK)
        compact_pill(b,520,y+8,f'选项{i%2+1}',TINT,w=48)
        b.circle(730,y+16,8,'#e0e8f0')
        b.text(746,y+21,'示例成员',11.5)
        b.text(960,y+21,'示例数据',11.5,MUTED)
        b.text(1180,y+21,'示例数据' if i!=1 else '示例数据…',11.5,MUTED)
    b.text(225,ybottom+23,'+',19,FAINT)
    b.line(SIDEBAR,ybottom+32,WIDTH,ybottom+32)
    b.line(SIDEBAR,892,WIDTH,892)
    b.text(291,909,'3 条记录',10.5,MUTED)
    b.line(344,904,348,908,MUTED,.8)
    b.line(348,908,352,904,MUTED,.8)
    if selected:
        b.rect(1170,y0+hh,430,rh,'none',BLUE,1)
    b.anchor('table-header',204,128,1396,30)
    b.anchor('grid-body',204,158,1396,96)
    b.anchor('selected-cell',1170,158,430,32)
    b.anchor('toolbar-field-config',321,99,81,25)


def desktop_grid():
    b=Board('desktop-grid','数据表页面',['数据表预览','字段配置入口','单元格与记录'],width=1600,height=924)
    chrome(b,active='表格',tools=[('字段配置','table'),('视图配置','table'),('筛选','filter'),('分组','gallery'),('排序','text'),('行高','text'),('填色','chart')])
    grid_content(b)
    return b


def kanban():
    b=Board('kanban','看板视图',['分组卡片预览','记录详情入口'],width=1600,height=924)
    chrome(b,active='看板',tools=[('分组依据 单选1','select'),('卡片配置','table'),('筛选','filter'),('排序','text')])
    xs=[222,502,782]
    fills=['#fcf8ed','#edf9f7','#f7f3fc']
    for ci,(x,(group,pillfill),fill) in enumerate(zip(xs,GROUPS,fills)):
        empty=ci==2
        b.rect(x,130,262,64 if empty else 300,fill,radius=8)
        compact_pill(b,x+10,138,group,pillfill,w=61)
        b.text(x+82,151,0 if empty else 1,11,FAINT)
        if empty:
            b.text(x+125,180,'+',20,FAINT)
            continue
        cardx,cardy=x+7,162
        b.rect(cardx,cardy,248,226,WHITE,LINE,5)
        b.text(cardx+11,187,'示例数据',12,INK,600)
        field_label(b,cardx+11,218,'文本1：')
        b.text(cardx+11,242,'示例数据',11.5)
        field_label(b,cardx+11,278,'单选1：','choice')
        compact_pill(b,cardx+80,265,f'选项{ci+1}',TINT,w=48)
        field_label(b,cardx+11,314,'文本2：')
        b.text(cardx+11,340,'示例数据…',11.5,MUTED)
        b.text(cardx+11,360,'示例数据…',11.5,MUTED)
        b.text(x+125,419,'+',20,FAINT)
        b.anchor(f'kanban-card-{ci+1}',cardx,cardy,248,226)
    b.anchor('kanban-groups',222,130,826,300)
    b.anchor('kanban-target-field',240,300,220,65)
    return b


def calendar():
    b=Board('calendar','日历视图',['月视图预览','日程块与记录入口'],width=1600,height=924)
    chrome(b,active='日历',tools=[('日程块配置','table'),('日历配置','calendar'),('筛选','filter')])
    b.button(225,138,'今天',False,38,22)
    b.text(285,154,'‹',20,FAINT)
    b.text(319,154,'›',20,FAINT)
    b.text(353,153,'2026年11月',12,INK,550)
    b.line(441,148,445,152,MUTED,.8)
    b.line(445,152,449,148,MUTED,.8)
    b.rect(1459,137,125,24,'#f3f4f5',radius=5)
    for i,label in enumerate(['日','周','月']):
        if i==2:b.rect(1542,138,41,22,WHITE,LINE,4)
        b.text(1475+42*i,153,label,11.5,MUTED)
    cw=(WIDTH-SIDEBAR)/7
    for i,label in enumerate(['周一','周二','周三','周四','周五','周六','周日']):
        b.text(228+cw*i,185,label,12,MUTED)
    y0,rh=197,120.5
    for row in range(7): b.line(SIDEBAR,y0+rh*row,WIDTH,y0+rh*row)
    days=[26,27,28,29,30,31,1]+list(range(2,31))+list(range(1,7))
    for idx,day in enumerate(days):
        row,col=divmod(idx,7)
        x=228+col*cw;y=y0+row*rh
        current=not (idx<6 or idx>=36)
        label='11月1日' if idx==6 else '12月1日' if idx==36 else str(day)
        if idx==16:
            b.circle(x+5,y+12,10,BLUE)
            b.text(x-1,y+17,'11',10.5,WHITE,600)
        else:b.text(x,y+17,label,11.5,INK if current else FAINT)
    events=[(11,0),(14,0)]
    for idx,slot in events:
        row,col=divmod(idx,7)
        x=SIDEBAR+cw*col+3;y=y0+row*rh+25+slot*21
        b.rect(x,y,cw-12,18,'#edf1fd',radius=3)
        b.rect(x,y,2,18,'#7694ef',radius=1)
        b.text(x+7,y+13,'示例数据',10.5,INK)
    b.anchor('calendar-month-controls',225,137,1359,29)
    b.anchor('calendar-grid',204,197,1396,723)
    b.anchor('calendar-event',1004,342.5,187.4,18)
    return b


def gantt():
    b=Board('gantt','甘特图视图',['时间轴预览','任务条与记录入口'],width=1600,height=924)
    chrome(b,active='甘特图',tools=[('字段配置','table'),('甘特图配置','gantt'),('筛选','filter'),('分组','gallery'),('排序','text')])
    split, ybottom = 410, 340
    b.line(split,128,split,ybottom)
    b.text(389,147,'≪',15,MUTED)
    b.text(420,147,'2026年6月',12,MUTED,550)
    b.text(523,147,'2026年7月',12,MUTED,550)
    for i,label in enumerate(['周','月','季','年']):
        if i==1:b.rect(1378,133,22,22,TINT,radius=4)
        b.text(1353+i*32,149,label,12,BLUE if i==1 else MUTED)
    b.line(1475,134,1475,151)
    b.text(1495,149,'今天',12,MUTED)
    b.text(1540,149,'‹',18,MUTED)
    b.text(1574,149,'›',18,MUTED)
    b.rect(227,176,11,11,'none',MUTED,1)
    field_label(b,261,186,'文本1','text',11.5)
    ncols=23;cw=(WIDTH-split)/ncols
    labels=[29,30]+list(range(1,22))
    for i,label in enumerate(labels):
        x=split+cw*i
        b.text(x+18,187,str(label),10.5,FAINT)
        if i%7 in (5,6):b.rect(x,196,cw,ybottom-196,'#f4f4f5')
        b.line(x,196,x,ybottom)
    b.line(SIDEBAR,196,WIDTH,196)
    b.line(SIDEBAR,ybottom,WIDTH,ybottom)
    for i,offset in enumerate((3,5,8)):
        y=196+36*i
        b.text(229,y+21,i+1,11,FAINT)
        b.text(261,y+21,'示例数据',11.5)
        x=split+cw*offset
        b.rect(x+1,y+1,cw-2,25,'#48a95b',radius=5)
        b.text(x+18,y+18,'1天',11,WHITE)
        b.text(x+cw+8,y+18,'示例数据',11.5)
    b.text(225,331,'+',18,FAINT)
    b.rect(743,344,88,5,'#b9bdc3',radius=2)
    b.anchor('gantt-records',204,196,206,108)
    b.anchor('gantt-timeline',410,196,1190,144)
    b.anchor('gantt-task-bar',566.2,197,49.7,25)
    b.anchor('gantt-header',410,128,1190,68)
    return b


def gallery():
    b=Board('gallery','画册视图',['多列卡片预览','记录详情入口'],width=1600,height=924)
    chrome(b,active='画册',tools=[('卡片配置','table'),('筛选','filter'),('排序','text')])
    cw,ch,gap=262,216,14
    for col in range(3):
        x=218+col*(cw+gap);y=130
        b.rect(x,y,cw,ch,WHITE,LINE,7)
        b.text(x+15,y+27,'示例数据',13,INK,550)
        field_label(b,x+15,y+56,'文本1：')
        b.text(x+15,y+81,'示例数据',12)
        field_label(b,x+15,y+111,'单选1：','choice')
        compact_pill(b,x+86,y+98,f'选项{col%2+1}',TINT,w=63)
        field_label(b,x+15,y+141,'文本2：')
        b.text(x+15,y+166,'示例数据…',12,MUTED)
    b.anchor('gallery-grid',218,130,814,216)
    b.anchor('gallery-card',218,130,262,216)
    b.anchor('gallery-target-field',233,178,232,44)
    return b


def build_all():
    return [desktop_grid(),kanban(),calendar(),gantt(),gallery()]

if __name__=='__main__':
    for board in build_all():
        board.write()
