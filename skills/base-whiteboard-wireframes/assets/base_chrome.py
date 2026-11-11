#!/usr/bin/env python3
"""Editable Base chrome, redrawn from the supplied desktop references."""
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT, SIDEBAR = 1600, 924, 204
INK, MUTED, FAINT = '#30343b', '#707782', '#a1a6af'
LINE, PANEL, BG, WHITE = '#dfe2e7', '#f6f7f9', '#f1f2f4', '#ffffff'
BLUE, TINT = '#245bdb', '#eef2ff'

class Board:
    def __init__(self, key, title, scenarios, width=WIDTH, height=HEIGHT):
        self.key, self.width, self.height = key, width, height
        self.nodes = []
        self.meta = dict(id=key, title=title, svg=f'{key}.svg', png=f'{key}.png',
                         scenarios=scenarios, width=width, height=height, anchors={})
        self.rect(0, 0, width, height)
    def anchor(self, name, x, y, width, height):
        assert x >= 0 and y >= 0 and x+width <= self.width and y+height <= self.height, (self.key,name)
        self.meta['anchors'][name] = dict(x=x,y=y,width=width,height=height)
    def rect(self,x,y,w,h,fill=WHITE,stroke='none',radius=0,sw=1,opacity=None):
        alpha = '' if opacity is None else f' opacity="{opacity}"'
        self.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{alpha}/>')
    def line(self,x,y,x2,y2,color=LINE,sw=1):
        self.nodes.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')
    def circle(self,x,y,r,fill=BLUE,stroke='none',sw=1):
        self.nodes.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self,x,y,value,size=12,color=INK,weight=400):
        self.nodes.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="PingFang SC, Noto Sans SC, Microsoft YaHei, sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>')
    def pill(self,x,y,label,fill=TINT,ink=INK,w=None):
        w = w if w is not None else len(label)*11+14
        self.rect(x,y,w,18,fill,radius=8)
        self.text(x+7,y+13,label,11,ink,550)
    def button(self,x,y,label,primary=False,w=74,h=28):
        self.rect(x,y,w,h,BLUE if primary else WHITE,'none' if primary else LINE,5)
        self.text(x+10,y+h/2+4,label,12,WHITE if primary else INK,500)
    def icon(self,name,x,y,size=13,color=MUTED):
        s=size; c=color
        if name in ('table','grid'):
            self.rect(x,y,s,s,'none',c,1)
            self.line(x,y+s*.33,x+s,y+s*.33,c)
            self.line(x,y+s*.66,x+s,y+s*.66,c)
            self.line(x+s*.33,y,x+s*.33,y+s,c)
        elif name=='calendar':
            self.rect(x,y+2,s,s-2,'none',c,2)
            self.line(x,y+5,x+s,y+5,c)
            self.line(x+3,y,x+3,y+4,c)
            self.line(x+s-3,y,x+s-3,y+4,c)
            for dx in (4,8):
                for dy in (8,11): self.circle(x+dx,y+dy,.65,c)
        elif name=='kanban':
            for dx,hh in ((0,10),(5,13),(10,7)): self.rect(x+dx,y,3,hh,'none',c,.5)
        elif name=='gantt':
            for dx,dy,ww in ((3,0,9),(0,5,9),(4,10,9)): self.rect(x+dx,y+dy,ww,3,'none',c,1)
        elif name=='gallery':
            for dx in (0,7):
                for dy in (0,7): self.rect(x+dx,y+dy,5,5,'none',c,1)
        elif name=='form':
            self.rect(x+1,y,s-2,s,'none',c,1)
            self.line(x+4,y+4,x+6,y+6,c); self.line(x+6,y+6,x+10,y+2,c)
            self.line(x+4,y+10,x+10,y+10,c)
        elif name=='search':
            self.circle(x+5,y+5,4,'none',c); self.line(x+8,y+8,x+12,y+12,c)
        elif name=='filter':
            for p,q in [((0,1),(13,1)),((13,1),(8,7)),((8,7),(8,13)),((8,13),(5,11)),((5,11),(5,7)),((5,7),(0,1))]:self.line(x+p[0],y+p[1],x+q[0],y+q[1],c)
        elif name=='person':
            self.circle(x+6,y+3,3,'none',c); self.rect(x+1,y+8,11,5,'none',c,2)
        elif name=='select':
            self.circle(x+6,y+6,6,'none',c); self.line(x+3,y+5,x+6,y+8,c);self.line(x+6,y+8,x+9,y+5,c)
        elif name=='check':
            self.rect(x,y,s,s,'none',c,1);self.line(x+3,y+6,x+6,y+9,c);self.line(x+6,y+9,x+10,y+3,c)
        elif name=='plus':
            self.line(x+s/2,y,x+s/2,y+s,c); self.line(x,y+s/2,x+s,y+s/2,c)
        elif name=='workflow':
            for dx,dy in ((5,0),(0,9),(10,9)):self.circle(x+dx+1,y+dy+1,2,'none',c)
            self.line(x+6,y+3,x+6,y+6,c);self.line(x+1,y+6,x+11,y+6,c);self.line(x+1,y+6,x+1,y+8,c);self.line(x+11,y+6,x+11,y+8,c)
        elif name=='chart':
            self.circle(x+6,y+6,6,'none',c);self.line(x+6,y,x+6,y+6,c);self.line(x+6,y+6,x+11,y+9,c)
        elif name=='text':
            self.text(x,y+12,'A',14,c)
            for dy in (3,7,11):self.line(x+10,y+dy,x+14,y+dy,c)
        elif name=='chevron':
            self.line(x+3,y+3,x+7,y+6,c);self.line(x+7,y+6,x+3,y+9,c)
        elif name=='lock':
            self.rect(x+2,y+5,9,8,'none',c,1);self.rect(x+4,y,5,6,'none',c,2)
        elif name=='more':
            for dx in (1,6,11):self.circle(x+dx,y+6,1,c)
        else:
            self.rect(x+1,y+1,s-2,s-2,'none',c,2)
            self.line(x+4,y+5,x+s-4,y+5,c);self.line(x+4,y+8,x+s-4,y+8,c)
    def write(self):
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">\n'+ '\n'.join(self.nodes)+'\n</svg>\n'
        (HERE/self.meta['svg']).write_text(svg,encoding='utf-8')

NAV=[('table','门店档案与经营目标表'),('table','产品物料与供应商表'),('table','订货库存与损耗表'),('table','会员客诉与服务工单表'),('table','财务结算与经营分析表'),('chart','总部经营驾驶舱'),('form','收集表'),('form','收集表 2'),('table','新品与营销活动表'),('form','收集表 3'),('search','查询页'),('table','数据表 2'),('workflow','数据变动提醒工作流'),('chart','库存与损耗数据分析'),('form','收集表 4'),('form','文档'),('form','收集表 5'),('form','品牌展示页'),('table','数据表 3'),('chart','数据表 3 数据表现'),('table','测试数据'),('table','测试数据 1')]

def chrome(b,active='表格',mode='views',selected='门店档案与经营目标表',toolbar=True,tools=None):
    b.rect(0,0,WIDTH,56,WHITE)
    b.line(0,55,WIDTH,55)
    for dy in (18,22,26):b.line(18,dy,29,dy,MUTED)
    b.icon('table',47,18,12)
    b.text(87,25,'示例空间  ›  业务管理  ›  协作项目  ›',12,MUTED)
    b.rect(434,14,13,13,'#a16ae8',radius=3)
    b.text(454,25,'示例经营协同系统',13,INK,550)
    b.text(87,43,'已保存到云端     |     最近修改：刚刚',10,FAINT)
    b.button(1098,13,'分享',True,68)
    b.button(1177,13,'自动化',False,77)
    for i,name in enumerate(('lock','more','search','plus')):b.icon(name,1274+i*34,20,13)
    for x1,y1,x2,y2 in ((1426,17,1426,31),(1419,24,1433,24),(1422,20,1430,28),(1422,28,1430,20)):
        b.line(x1,y1,x2,y2,MUTED,1)
    b.text(1440,30,'问问 AI',12,INK)
    b.circle(1570,26,13,'#dce5f5');b.text(1566,30,'A',11,MUTED)
    b.rect(0,56,SIDEBAR,HEIGHT-56,WHITE)
    b.line(SIDEBAR,56,SIDEBAR,HEIGHT)
    b.icon('search',17,69);b.text(35,80,'搜索',12,FAINT);b.icon('plus',149,70);b.text(182,80,'≪',14,FAINT)
    b.icon('form',17,100);b.text(35,112,'示例经营协同系统…',12,INK)
    b.text(19,145,'›  文件夹',12,MUTED)
    for i,(ico,label) in enumerate(NAV):
        yy=160+i*32.5
        if yy+29>880:break
        active_item=label==selected
        if active_item:b.rect(9,yy-3,184,30,TINT,radius=5)
        b.icon(ico,18,yy+6,12,BLUE if active_item else MUTED)
        label=label if len(label)<=13 else label[:12]+'…'
        b.text(35,yy+17,label,12,BLUE if active_item else INK)
    b.button(10,884,'＋ 新建',False,183,28)
    b.anchor('sidebar',0,56,SIDEBAR,868)
    b.anchor('topbar',0,0,WIDTH,56)
    if mode in ('workflow','dashboard'):return
    b.rect(SIDEBAR,56,WIDTH-SIDEBAR,40,PANEL)
    tabs=[('table','全部门店经营总览','表格',154),('kanban','区域优秀门店','看板',132),('calendar','日历','日历',84),('gantt','甘特图','甘特图',85),('gallery','画册','画册',78),('form','表单','表单',79)] if mode!='survey' else [('form','收集表','收集表',104),('table','收集结果','收集结果',110)]
    xx=SIDEBAR+10
    for ico,label,key,ww in tabs:
        chosen=(key==active)
        if chosen:b.rect(xx,57,ww,39,WHITE,radius=6)
        b.icon(ico,xx+12,68,12,BLUE if chosen else MUTED)
        b.text(xx+32,80,label,12,INK if chosen else MUTED,500 if chosen else 400)
        xx+=ww
    b.icon('plus',xx+15,69,12)
    b.line(SIDEBAR,96,WIDTH,96)
    b.anchor('view-tabs',SIDEBAR,56,WIDTH-SIDEBAR,40)
    if not toolbar:return
    b.text(224,116,'＋ 添加记录',12,BLUE)
    entries=tools if tools is not None else [('字段配置','table'),('视图配置','table'),('筛选','filter'),('分组','gallery'),('排序','text'),('行高','text'),('填色','chart')]
    xx=326
    for item in entries:
        label,ico=item if isinstance(item,(tuple,list)) else (item,'table')
        b.icon(ico,xx,105,12)
        b.text(xx+18,116,label,12,MUTED)
        if label=='字段配置':b.anchor('toolbar-field-config',xx-5,99,81,26)
        xx+=len(label)*12+41
    b.text(1230,116,'智能提醒    生成页面',11,FAINT)
    for i,name in enumerate(('form','more','search')):b.icon(name,1462+i*42,105,12)
    b.line(SIDEBAR,128,WIDTH,128)
    b.anchor('toolbar',SIDEBAR,96,WIDTH-SIDEBAR,32)
    b.anchor('view-canvas',SIDEBAR,128,WIDTH-SIDEBAR,HEIGHT-128)

def dim(b):b.rect(0,0,b.width,b.height,'#1f2633',opacity=.35)
