#!/usr/bin/env python3
"""Companion dialogs on the screenshot-aligned Base data-table shell."""
from base_chrome import *
from build_view_templates import grid_content

def grid(b):
    chrome(b)
    grid_content(b)

def config_panel(b):
    b.rect(580,157,298,300,WHITE,LINE,5)
    b.text(594,180,'标题',12,MUTED)
    b.rect(594,189,270,29,WHITE,LINE,4)
    b.text(604,209,'文本 5',12)
    b.text(594,245,'字段类型',12,MUTED)
    b.rect(594,255,270,59,WHITE,LINE,4)
    b.icon('text',604,265);b.text(626,278,'文本',12)
    b.icon('chevron',844,265)
    b.rect(595,287,268,26,PANEL)
    b.text(605,305,'探索字段捷径',11,MUTED)
    b.text(594,341,'默认值',12,MUTED)
    b.rect(594,351,270,29,WHITE,LINE,4)
    b.text(604,371,'请输入默认值',12,FAINT)
    b.button(710,414,'取消',False,69)
    b.button(789,414,'确定',True,75)
    b.anchor('field-config',580,157,298,300)
    b.anchor('field-type',594,255,270,33)
    b.anchor('default-value',594,332,270,48)
    b.anchor('field-config-actions',705,409,164,37)

def field_config():
    b=Board('field-config','文本字段配置',['字段标题、类型和默认值'])
    grid(b);config_panel(b)
    return b

def field_picker():
    b=Board('field-picker','字段类型选择',['字段配置中选择类型','同框架下比较字段方案'])
    grid(b);config_panel(b)
    b.rect(881,157,334,576,WHITE,LINE,5)
    b.icon('search',897,174);b.text(920,186,'搜索字段类型',12,FAINT)
    b.line(881,202,1215,202)
    b.text(897,226,'AI 字段',11,FAINT)
    for i,label in enumerate(('智能体','翻译','分类','总结')):
        x=897+(i%2)*155;y=246+(i//2)*32
        b.icon('form',x,y);b.text(x+23,y+11,label,12,MUTED)
    b.line(895,309,1202,309)
    b.text(897,333,'常规',11,FAINT)
    labels=[('text','文本'),('table','附件'),('select','单选'),('text','数字'),('check','多选'),('check','复选框'),('person','人员'),('text','超链接'),('calendar','日期'),('search','查找引用')]
    for i,(ico,label) in enumerate(labels):
        x=897+(i%2)*155;y=348+(i//2)*32
        if i==0:b.rect(x-5,y-5,140,26,TINT,BLUE,3)
        b.icon(ico,x,y,12,BLUE if i==0 else MUTED);b.text(x+23,y+11,label,12)
    b.line(895,518,1202,518);b.text(897,540,'业务',11,FAINT)
    for i,label in enumerate(('流程','条码','按钮','签名','自动编号','进度')):
        x=897+(i%2)*155;y=557+(i//2)*32
        b.icon('form',x,y);b.text(x+23,y+11,label,12,MUTED)
    b.line(895,659,1202,659);b.text(897,681,'高级',11,FAINT)
    b.text(898,712,'单向关联                双向关联',12,MUTED)
    b.anchor('field-picker',881,157,334,576)
    b.anchor('field-picker-option',892,343,140,26)
    return b

def record_detail():
    b=Board('record-detail','记录详情',['字段预览与直接编辑','展开 Doc 编辑器'])
    grid(b)
    b.rect(870,56,730,868,WHITE,LINE)
    b.text(895,85,'记录详情',12,MUTED);b.text(1460,85,'上一条  下一条',11,MUTED);b.text(1570,85,'×',20,MUTED)
    b.line(870,101,1600,101)
    b.text(898,148,'示例上海静安店',23,INK,600)
    b.text(898,186,'详情',13,BLUE);b.text(953,186,'活动',13,MUTED)
    b.line(898,197,1572,197);b.line(898,197,926,197,BLUE,2)
    for i,(label,value) in enumerate((('门店编号','STORE-SH-001'),('门店类型','直营'),('所属区域','华东一区'),('城市','上海'),('门店负责人','成员 A'))):
        y=236+i*48;b.text(900,y,label,12,MUTED);b.text(1092,y,value,13)
    b.text(900,486,'经营摘要',12,MUTED)
    b.rect(1080,467,486,255,WHITE,LINE,5)
    b.text(1096,498,'本周经营情况',17,INK,600)
    b.text(1096,532,'补充门店经营摘要，记录关键问题和后续行动。',13)
    b.text(1096,564,'• 跟进活动执行与库存情况',13)
    b.text(1096,594,'• 查看相关说明',13,BLUE)
    b.rect(1096,617,151,74,PANEL,LINE,3);b.text(1140,661,'图片预览',12,MUTED)
    b.rect(1532,475,25,25,WHITE,LINE,4)
    for x,y,xx,yy in ((1538,481,1543,481),(1538,481,1538,486),(1551,494,1546,494),(1551,494,1551,489)):b.line(x,y,xx,yy,MUTED)
    b.text(900,771,'创建时间',12,MUTED);b.text(1092,771,'2026/11/01 10:00',13)
    b.rect(894,869,675,35,PANEL,radius=5);b.text(910,891,'输入评论',12,FAINT)
    b.anchor('detail-panel',870,56,730,868)
    b.anchor('detail-target-field',1080,467,486,255)
    b.anchor('detail-expand',1532,475,25,25)
    return b

def editor_modal():
    b=Board('editor-modal','Doc 编辑弹窗',['展开富文本编辑','保存与取消'])
    grid(b);dim(b)
    b.rect(400,165,800,587,WHITE,LINE,8)
    b.text(423,198,'经营摘要',16,INK,600);b.text(1167,198,'×',20,MUTED)
    b.line(400,216,1200,216)
    b.rect(420,231,760,38,PANEL,LINE,4)
    for i,label in enumerate(('正文','B','I','U','S','列表','引用','代码','链接','图片','颜色')):
        x=431+i*66;b.text(x,255,label,12,INK,600 if label=='B' else 400)
    b.text(433,310,'本周经营情况',21,INK,600)
    b.text(433,352,'补充门店经营摘要，记录关键问题和后续行动。',14)
    b.text(433,389,'• 跟进活动执行与库存情况',14)
    b.text(433,423,'• 查看相关说明',14,BLUE)
    b.rect(433,453,267,145,PANEL,LINE,5);b.text(532,534,'图片预览',13,MUTED)
    b.line(400,688,1200,688);b.button(1020,710,'取消',False,70);b.button(1102,710,'保存',True,75)
    for name,x,y,w,h in (('editor-modal',400,165,800,587),('editor-toolbar',420,231,760,38),('editor-content',421,278,757,392),('editor-actions',1014,703,170,39)):
        b.anchor(name,x,y,w,h)
    return b

def excel_import_map():
    b=Board('excel-import-map','Excel 追加导入映射',['字段映射','导入前确认'])
    grid(b);dim(b)
    b.rect(310,139,980,651,WHITE,LINE,8)
    b.text(336,179,'追加导入 Excel',18,INK,600);b.text(1259,177,'×',20,MUTED)
    for i,label in enumerate(('1 选择文件','2 匹配字段','3 确认导入')):
        b.rect(336+i*230,204,200,34,TINT if i==1 else PANEL,radius=4)
        b.text(350+i*230,226,label,13,BLUE if i==1 else MUTED)
    b.text(337,279,'示例导入.xlsx     工作表：门店清单',13)
    b.text(926,279,'目标数据表：门店档案表',13,MUTED)
    b.rect(337,300,926,328,WHITE,LINE,5);b.rect(338,301,924,39,PANEL)
    for x,label in ((354,'Excel 列'),(651,'示例值'),(953,'Base 字段')):b.text(x,325,label,12,MUTED)
    for x in (633,934):b.line(x,300,x,628)
    for i,(label,value) in enumerate((('门店编号','STORE-SH-001'),('门店名称','示例上海静安店'),('所属区域','华东一区'),('城市','上海'))):
        y=340+i*72;b.line(337,y,1263,y);b.text(354,y+43,label,13);b.text(651,y+43,value,13)
        b.rect(951,y+18,291,36,WHITE,LINE,4);b.text(964,y+42,label,13);b.icon('chevron',1221,y+29)
    b.text(337,663,'当前匹配 4 列，可在确认导入前检查字段和记录预览。',12,MUTED)
    b.line(310,719,1290,719);b.button(337,743,'上一步',False,82);b.button(1083,743,'取消',False,72);b.button(1167,743,'下一步',True,96)
    b.anchor('import-modal',310,139,980,651);b.anchor('import-mapping',337,300,926,328)
    b.anchor('mapping-target',951,358,291,36);b.anchor('import-actions',1076,738,187,41)
    return b

def build_all():return [field_picker(),field_config(),record_detail(),editor_modal(),excel_import_map()]
