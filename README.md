# Примеры кода

https://card-sfera.online/map/  Мини-проект на Django

## obs2matrix.py
Каждое наблюдение описывается тройкой ('param_row', 'param_col', value). Наблюдения хранится (в файле или переменной) в виде списка. Необходимо представить наблюдения в виде матрицы.

## xmlparse.py
Ключ - тэг элемента (корневого элемента запись или вложенного элемента любого уровня).

Значение - словарь, состоящий из атрибутов данного тэга

Если xml-запись содержит последовательность одинаковых тэгов с различными значениями атрибутов, то парсер объединяет их в список. 

Парсер задуман для промежуточного преобразования данных xml в базу данных 

Поскольку каждая запись имеет двухуровневую структуру (значения ключей не плоские объекты а словари). была добавлена опциональная фишка для преобразования записей в плоскую структуру для упрощения закгузки данных в БД. Правила преобразования:
- значение ключа разворачивается за счет добавления в качестве префикса имени ключа
- если значение ключа - список dict, то сначала все значения каждого dict склеиваются в строку, разделяясь "#", а затем все эти строки списка также склеиваются в одну строку, разделяясь "###"

Включить создание плоской структуры можно установив флаг. FLAT_RECORD

Пользоваться этой фишкой или нет - зависит от конкретной решаемой задачи

На выходе получаем json файл. Одна строка - одна запись в формате json (dict)

Если FLAT_RECORD включен, дополнительно подсчитывается и выводится статистика по каждому ключу: - имя ключа, количество упоминаний во всех записях, максимальная длина значения ключа (как строкового выражения)

