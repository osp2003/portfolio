
# -*- coding: utf-8 -*-
from os import listdir
from lxml import etree
import json
# входные параметры скрипта
PATH='c:\\tmp\\1'               # каталог с xml-файлами
RECORD_TAG='Документ'           # тэг корневого элемента записи
COUNT=-1                         # количество файлов для парсинга (-1 все файлы каталога)
SAVE2FILE='result_all2.json'        # файл гезультата парсинга
EXCUDE_TAGS=['Файл', 'ФИООтв']  # тэги, которые не нужно парсить
FLAT_RECORD=True                # преобразовать запись в плоскую
def flatRecord(rec):
    record={}
    for k,v in rec.items():
        if isinstance(v, dict):
            record.update({k+'_'+i: v[i] for i in v})
            continue
        record[k]='###'.join(['#'.join(i.values()) for i in v])
    return record
def getTreeByXml(file_object):
    record={}
    context = etree.iterparse(file_object, events=("start","end"))
    for event, elem in context:
        attrib=dict(elem.attrib)
        tag=etree.QName(elem.tag).localname
        if not attrib or tag in EXCUDE_TAGS:
            continue
        if event=="end" and tag==RECORD_TAG:
            yield flatRecord(record) if FLAT_RECORD else record
            elem.clear()
            record={}
            continue
        record.setdefault(tag, attrib)
        if record[tag] != attrib:
            try:
                record[tag].append(attrib)
            except:
                record[tag]=[record[tag], attrib]
stat={}
def addToStat(rec, stat=stat):
    for k in rec.keys():
        v=stat.setdefault(k,[0,0])
        stat[k][0]+=1
        if len(rec[k])>v[1]:
            stat[k][1]=len(rec[k])
fw=open(SAVE2FILE, 'w', encoding='utf-8')
for f in listdir(PATH): 
    if not COUNT:
        break
    fr=open(PATH+'\\'+f,'rb')
    for rec in getTreeByXml(fr):
        if FLAT_RECORD:
            addToStat(rec)
        fw.write(json.dumps(rec, ensure_ascii=False)+'\n')
    fr.close()
    print (COUNT)
    COUNT-=1
fw.close()
if FLAT_RECORD:
    for k,v in stat.items():
        print ('%s: %d, %d' % (k, v[0], v[1]))
