
import pandas as pd
import os
from xlsxwriter.workbook import Workbook
from Costanti import *
"""
Creazione Directory definite in Costanti.py
"""
for path in [INPUT_PATH_CSV, INPUT_PATH_XLSX, OUTPUT_PATH_ID_INC, LOG_PATH]:
    sub_path = path.split("/")
    actual_path = "./"
    for path in sub_path:
        actual_path += path + "/"
        if not os.path.isdir(actual_path):
            os.mkdir(actual_path)
"""
    I file xls non riescono ad essere aperti dalle librerie di python, quindi li rinomino in csv
    per risolvere il problema
"""

for file in os.listdir(INPUT_PATH_CSV):
    if not file.endswith('.xls'):
        continue
    try:
        os.rename(f"{INPUT_PATH_CSV}/{file}", f"{INPUT_PATH_CSV}/{file[:-4]}.csv")
    except FileExistsError:
        pass

"""
    Creazione file xlsx da csv
"""
log = open(f'{LOG_PATH}/csv_log.txt', 'w')
for file in os.listdir(INPUT_PATH_CSV):
    if not file.endswith('.csv'):
        continue
    try:
        res = pd.read_csv(f"{INPUT_PATH_CSV}/{file}", delimiter='\t', encoding='ISO-8859-1')
        labels = res.columns.array


        workbook = Workbook(f"{INPUT_PATH_XLSX}/{file[:-4]}.xlsx")
        worksheet = workbook.add_worksheet()
        for i, l in enumerate(labels):
            worksheet.write(0, i, l)
        for r, row in enumerate(res.values):
            for c, val in enumerate(row):
                worksheet.write(r+1, c, val if type(val) != float else 'N')
        workbook.close()
    except Exception as e:
        log.write(f"FILE :[{file}] HA DATO ERRORE {e}\n")

'''REMOVE CSV OF EXISTING XLSX FILES'''
for file in os.listdir(INPUT_PATH_XLSX):
    if not file.endswith('.xlsx'):
        continue
    try:
        os.remove(f'{INPUT_PATH_CSV}/{file[:-5]}.csv')
    except:
        log.write('ERRORE', file)

log.close()
