# -*- coding: utf-8 -*-
import re
from pyparsing import Word, alphas, ZeroOrMore, Optional, Literal, Group, Suppress
def parserQuery(query=''):
	if not query: return ''
	query=u''+query
	zamena=['A', 'B', 'C', 'D']
	#=== предварительная подготовка строки
	query=re.sub(ur'([^a-zA-Zа-яА-Я0-9ёЁ\'\"\;\,\(\)\ ]+)', '', query) # 
	query=re.sub(ur'[\'\"]+',"''",query)	# такая замена кавычек нужна для корректного запроса sql
	query=query.split(';')
	# ограничениями fts postgresql допустимо только 4 категории документов поиска - A,B,С,D
	# если в стоке поиска ';' задана больше - все лишние объединяются с последней по условию 'ИЛИ'
	if len(query)>4:
		for l in query[4:]:
			query[3]+=', '+l # если нужно будет заменить по условию 'И' - убрать запятую оставив пробел
	query=query[:4]
	
	#===парсер
	resp=[]
	for i in range(len(query)):
		if not query[i] or re.search(ur'^\s+$',query[i]): continue	# если блок пустой - пропускаем его
		s=_str4OneCategory(query[i], zamena[i])
		s=re.sub(ur'^\s*\&','',s)		# если строка tsquery начинается с & (пропущены обязательные слова)
		resp.append(s)
	return ' & '.join(resp)

#генерирует строку нужного формата из массива
def _strGen(arr=[], category='A'):
	if not arr: return ''

	for k in range(len(arr)):
		if type(arr[k])==type([]):
			arr[k]='('+(':'+category+' & ').join(arr[k])+':'+category+')'
	return ' | '.join(arr)

# на вход подается один блок данных и его метка, на выходе - строка формата tsquery
def _str4OneCategory(s='', category=''):
	if not s or not category: return ''

	rus_alphas = u'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
	token = Word(alphas+rus_alphas)
	obj=token+ZeroOrMore(token)
	templ_OR=Literal(',')
	templ_ANY=Literal('*')

	result=Optional(Group(obj)+ZeroOrMore(Suppress(templ_OR)+Group(obj))) # выделяет то, что надо искать

	result_Not=Optional(Suppress(result+Optional(templ_OR)+Optional(templ_ANY)+Literal('('))+result+Suppress(Literal(')'))) # выделяет то, что НЕ надо искать
	
	res=result.parseString(s).asList()
	res_not=result_Not.parseString(s).asList()
	s_not=_strGen(res_not, category)
	if not s_not:
		return _strGen(res, category)
	return _strGen(res, category)+' & !('+s_not+')'



if __name__ == "__main__":
	# пример использования
	s=u' дизельное топливо, бензин , (этилированный сухое); государственное учреждение ;;  (Краснодарский)'
	print parserQuery(s)


