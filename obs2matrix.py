import csv
import numpy as np

# загружаем данные частотного словаря
with open('tf-idf.csv','r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter=';')
    word_dict=np.array([[data[0], data[1],data[2]] for data in data_iter])

# генерируем категориальные оси столбцов и строк
row_ax=np.unique(word_dict[:,1])
col_ax=np.unique(word_dict[:,0])

# генерируем нулевую (пока) результирующую матрицу весов
m=np.zeros((len(row_ax), len(col_ax)))

# заполняем матрицу расчетными весами
a=np.where(row_ax==word_dict[:,1:2])[1]
b=np.where(col_ax==word_dict[:,:1])[1]
m[a,b]=word_dict[:,2]
print m
