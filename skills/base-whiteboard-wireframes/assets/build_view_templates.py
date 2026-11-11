#!/usr/bin/env python3
"""Screenshot-aligned Base table, kanban, calendar, gantt and gallery templates."""
from base_chrome import (Board, chrome, WIDTH, HEIGHT, SIDEBAR, INK, MUTED,
                         FAINT, LINE, PANEL, BG, WHITE, BLUE, TINT)

REGIONS = [('华东一区','#fbefc7'),('华南一区','#d9f2ed'),('华北一区','#f9e5e5'),('华东二区','#eee7fb')]
STORES = [
    ('STORE-SH-001','示例上海静安店','直营','华东一区','上海'),
    ('STORE-HZ-002','示例杭州湖滨店','直营','华东一区','杭州'),
    ('STORE-GZ-003','示例广州天河店','加盟','华南一区','广州'),
    ('STORE-BJ-004','示例北京望京店','直营','华北一区','北京'),
    ('STORE-SZ-005','示例深圳科技园店','加盟','华南一区','深圳'),
    ('STORE-SH-006','示例上海大学城店','快闪','华东二区','上海'),
]
COLS = [204,250,359,513,615,718,820,975,1129,1283,1385,1558,1600]


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
    y0,hh,rh = 128,30,27.4
    ybottom = y0+hh+21*rh
    b.rect(SIDEBAR,y0,WIDTH-SIDEBAR,hh,PANEL)
    for x in COLS:
        b.line(x,y0,x,ybottom)
    b.line(SIDEBAR,y0,WIDTH,y0)
    for i in range(22):
        b.line(SIDEBAR,y0+hh+i*rh,WIDTH,y0+hh+i*rh)
    b.rect(227,139,11,11,'none',MUTED,1)
    headers=[('门店编号','text'),('门店名称','text'),('门店类型','choice'),('所属区域','choice'),('城市','text'),('门店负责人','person'),('区域经理','person'),('文本 5','text'),('营业状态','choice'),('门店标签','text'),('开业日期','date')]
    for i,(label,kind) in enumerate(headers):
        # The partial date column at the viewport edge intentionally retains the scroll position.
        if i==10:
            field_label(b,COLS[i+1]+2,148,'日期','date',10)
        else:
            field_label(b,COLS[i+1]+6,148,label,kind,11.5)
    for i in range(21):
        y=y0+hh+i*rh
        b.text(229,y+18,str(i+1),11,FAINT)
        if i<6:
            code,name,typ,area,city=STORES[i]
            b.text(260,y+18,code,11.5,INK)
            b.text(367,y+18,name,11.5,INK)
            compact_pill(b,522,y+5,typ,('#e7ebfb' if typ=='直营' else '#fcebd8' if typ=='加盟' else '#d8f0f5'),w=37)
            rfill=dict(REGIONS)[area]
            compact_pill(b,623,y+5,area,rfill,w=64)
            b.text(726,y+18,city,11.5)
            for px in (829,984):
                b.circle(px+8,y+13,8,'#e0e8f0')
                b.text(px+22,y+18,'成员 A',11.5)
            compact_pill(b,1291,y+5,'营业中','#fbefc7',w=49)
            tags=[('商圈店','外卖占比高'),('商圈店','夜间营业'),('商圈店','新开店'),('写字楼店','外卖占比高'),('写字楼店','社群店'),('校园店','夜间营业')][i]
            compact_pill(b,1393,y+5,tags[0],'#e6ebfb',w=57 if len(tags[0])==4 else 47)
            compact_pill(b,1454,y+5,tags[1],'#f8ead9',w=min(88,len(tags[1])*11+12))
        elif i<18:
            b.text(260,y+18,'STORE-SH-006',11.5,INK)
            if i==6:
                b.text(367,y+18,'示例上海大学城店…',11.5,INK)
                compact_pill(b,522,y+5,'直营','#e7ebfb',w=37)
        if i==20:
            compact_pill(b,623,y+5,'华东二区','#eee7fb',w=64)
        if i<18:
            b.text(1565,y+18,'2026/',10.5,MUTED)
    b.text(225,ybottom+21,'+',19,FAINT)
    b.line(SIDEBAR,ybottom+28,WIDTH,ybottom+28)
    b.line(SIDEBAR,892,WIDTH,892)
    b.text(291,909,'21 条记录',10.5,MUTED)
    b.line(350,904,354,908,MUTED,.8)
    b.line(354,908,358,904,MUTED,.8)
    b.rect(205,916,483,5,'#b9bdc3',radius=2)
    if selected:
        b.rect(1129,y0+hh,154,rh,'none',BLUE,1)
    b.anchor('table-header',204,128,1396,30)
    b.anchor('grid-body',204,158,1396,575)
    b.anchor('selected-cell',1129,158,154,27.4)
    b.anchor('viewport-scrollbar',204,914,1396,9)
    b.anchor('toolbar-field-config',321,99,81,25)


def desktop_grid():
    b=Board('desktop-grid','数据表页面',['数据表预览','字段配置入口','单元格与记录'],width=1600,height=924)
    chrome(b,active='表格',tools=[('字段配置','table'),('视图配置','table'),('筛选','filter'),('分组','gallery'),('排序','text'),('行高','text'),('填色','chart')])
    grid_content(b)
    return b


def kanban():
    b=Board('kanban','看板视图',['分组卡片预览','记录详情入口'],width=1600,height=924)
    chrome(b,active='看板',tools=[('分组依据 所属区域','select'),('卡片配置','table'),('筛选','filter'),('排序','text')])
    xs=[222,448,674,900]
    fills=['#fcf8ed','#edf9f7','#fcf3f4','#f7f3fc']
    for ci,(x,(region,pillfill),fill) in enumerate(zip(xs,REGIONS,fills)):
        empty=ci==3
        b.rect(x,130,218,64 if empty else 778,fill,radius=8)
        compact_pill(b,x+10,138,region,pillfill,w=61)
        b.text(x+82,151,[2,1,1,0][ci],11,FAINT)
        if empty:
            b.text(x+103,180,'+',20,FAINT)
            continue
        cardx,cardy=x+7,162
        b.rect(cardx,cardy,204,714,WHITE,LINE,5)
        store=STORES[[0,4,3][ci]]
        code,name,typ,area,city=store
        b.text(cardx+11,187,code,12,INK,600)
        field_label(b,cardx+11,220,'门店名称：')
        b.text(cardx+11,244,name,11.5)
        field_label(b,cardx+11,272,'城市：')
        b.text(cardx+11,296,city,11.5)
        field_label(b,cardx+11,326,'门店类型：','choice')
        compact_pill(b,cardx+80,313,typ,'#e6ebfb' if typ=='直营' else '#fcebd8',w=35)
        field_label(b,cardx+11,355,'健康评分：','number')
        b.text(cardx+80,355,[74,74,52][ci],11.5)
        field_label(b,cardx+11,384,'目标达成率：','formula')
        b.text(cardx+92,384,['89.38%','108.80%','81.67%'][ci],11.5)
        field_label(b,cardx+11,413,'营业状态：','choice')
        compact_pill(b,cardx+80,400,'营业中','#fbefc7',w=48)
        field_label(b,cardx+11,442,'开业日期：','date')
        b.text(cardx+81,442,'2026/07/02',11.5)
        field_label(b,cardx+11,471,'月目标GMV：','number')
        b.text(cardx+91,471,['¥320,000','¥250,000','¥300,000'][ci],11.5)
        field_label(b,cardx+11,500,'本月GMV：','number')
        b.text(cardx+81,500,['¥286,000','¥272,000','¥245,000'][ci],11.5)
        field_label(b,cardx+11,529,'门店负责人：','person')
        b.circle(cardx+101,525,7,'#e0e8f0')
        b.text(cardx+113,529,'成员 A',11.5)
        field_label(b,cardx+11,558,'门店标签：','text')
        compact_pill(b,cardx+80,545,['商圈店','写字楼店','写字楼店'][ci],'#e6ebfb',w=60)
        compact_pill(b,cardx+144,545,'外卖高…','#f8ead9',w=52)
        field_label(b,cardx+11,588,'门店经营摘要：')
        b.text(cardx+11,614,['本月经营目标达成率 89.38%，','本月营业额持续增长，目标达成率','本月经营情况稳定，健康评分'][ci],11.2)
        b.text(cardx+11,633,['健康评分 74，需关注服务体验。…','108.80%，需持续跟进门店反馈。…','52，需持续改善门店服务体验。…'][ci],11.2)
        field_label(b,cardx+11,663,'区域经理：','person')
        b.circle(cardx+101,659,7,'#e0e8f0')
        b.text(cardx+113,663,'成员 A',11.5)
        field_label(b,cardx+11,692,'是否重点门店：','check')
        b.rect(cardx+123,681,12,12,'#64b66e' if ci!=1 else WHITE,LINE,2)
        if ci!=1:
            b.line(cardx+125,687,cardx+128,690,WHITE,1.2)
            b.line(cardx+128,690,cardx+133,684,WHITE,1.2)
        field_label(b,cardx+11,721,'新品与营销活动表：','link')
        b.rect(cardx+11,733,94,16,'#e7e9ec')
        b.text(cardx+18,745,'MKT-202607-02',10.5)
        field_label(b,cardx+11,779,'Last Modified Date：','date',10.5)
        b.text(cardx+11,799,'2026/11/11 16:13',10.5,MUTED)
        field_label(b,cardx+11,827,'Date Created 2：','date',10.5)
        b.text(cardx+11,848,'2026/07/02',10.5,MUTED)
        b.text(x+104,898,'+',20,FAINT)
        b.anchor(f'kanban-card-{ci+1}',cardx,cardy,204,714)
    b.anchor('kanban-groups',222,130,896,778)
    b.anchor('kanban-target-field',240,574,183,65)
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
    events=[(11,0),(11,1),(14,0)]
    for idx,slot in events:
        row,col=divmod(idx,7)
        x=SIDEBAR+cw*col+3;y=y0+row*rh+25+slot*21
        b.rect(x,y,cw-12,18,'#edf1fd',radius=3)
        b.rect(x,y,2,18,'#7694ef',radius=1)
        b.text(x+7,y+13,'未命名记录',10.5,INK)
    b.anchor('calendar-month-controls',225,137,1359,29)
    b.anchor('calendar-grid',204,197,1396,723)
    b.anchor('calendar-event',1004,342.5,187.4,18)
    return b


def gantt():
    b=Board('gantt','甘特图视图',['时间轴预览','任务条与记录入口'],width=1600,height=924)
    chrome(b,active='甘特图',tools=[('字段配置','table'),('甘特图配置','gantt'),('筛选','filter'),('分组','gallery'),('排序','text')])
    split=410
    b.line(split,128,split,797)
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
    field_label(b,261,186,'门店编号','text',11.5)
    ncols=23;cw=(WIDTH-split)/ncols
    labels=[29,30]+list(range(1,22))
    for i,label in enumerate(labels):
        x=split+cw*i
        b.text(x+18,187,str(label),10.5,FAINT)
        if i%7 in (5,6):b.rect(x,196,cw,601,'#f4f4f5')
        b.line(x,196,x,797)
    b.line(SIDEBAR,196,WIDTH,196)
    b.line(SIDEBAR,797,WIDTH,797)
    rh=27.4
    for i in range(21):
        y=196+rh*i
        b.text(229,y+18,str(i+1),11,FAINT)
        if i<18:b.text(261,y+18,STORES[i][0] if i<6 else 'STORE-SH-006',11.5)
        if i<6:
            x=split+cw*3
            b.rect(x+1,y+1,cw-2,25,'#48a95b',radius=5)
            b.text(x+18,y+18,'1天',11,WHITE)
            b.text(x+cw+8,y+18,STORES[i][1],11.5)
        elif i==6:
            x=split+cw*15
            b.rect(x+1,y+1,cw-2,25,'#48a95b',radius=5)
            b.text(x+18,y+18,'1天',11,WHITE)
        elif i<18:
            b.rect(1575,y+9,18,16,'#eef0f2',radius=3)
            b.text(1577,y+21,'→',15,MUTED)
    b.text(225,789,'+',18,FAINT)
    b.rect(743,800,88,5,'#b9bdc3',radius=2)
    b.anchor('gantt-records',204,196,206,575.4)
    b.anchor('gantt-timeline',410,196,1190,601)
    b.anchor('gantt-task-bar',566.2,197,49.7,25)
    b.anchor('gantt-header',410,128,1190,68)
    return b


def gallery():
    b=Board('gallery','画册视图',['多列卡片预览','记录详情入口'],width=1600,height=924)
    chrome(b,active='画册',tools=[('卡片配置','table'),('筛选','filter'),('排序','text')])
    cw,ch,gap=262,216,14
    for row in range(4):
        y=130+row*(ch+gap)
        for col in range(5):
            x=218+col*(cw+gap)
            h=min(ch,HEIGHT-y-2)
            b.rect(x,y,cw,h,WHITE,LINE,7)
            idx=row*5+col
            code=STORES[idx][0] if idx<6 else 'STORE-SH-006'
            b.text(x+15,y+27,code,13,INK,550)
            if idx<6:
                _,name,typ,area,city=STORES[idx]
                field_label(b,x+15,y+56,'门店名称：')
                b.text(x+15,y+81,name,12)
                field_label(b,x+15,y+111,'所属区域：','choice')
                compact_pill(b,x+86,y+98,area,dict(REGIONS)[area],w=63)
                field_label(b,x+15,y+141,'城市：')
                b.text(x+15,y+166,city,12)
            if row==3 and col>=3:
                b.rect(x+13,y+7,160,28,WHITE)
                b.text(x+15,y+27,'未命名记录',13,FAINT)
    b.anchor('gallery-grid',218,130,1366,792)
    b.anchor('gallery-card',218,130,262,216)
    b.anchor('gallery-target-field',233,178,232,44)
    return b


def build_all():
    return [desktop_grid(),kanban(),calendar(),gantt(),gallery()]

if __name__=='__main__':
    for board in build_all():
        board.write()
