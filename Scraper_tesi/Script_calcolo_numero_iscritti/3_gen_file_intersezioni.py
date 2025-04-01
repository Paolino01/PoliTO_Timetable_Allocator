import os
import pandas as pd
import xlsxwriter
from Costanti import *


mapIdIncToSetMatricole = {}
extractor_log = open(f'{LOG_PATH}/extractor_log.txt', 'w',encoding="utf-8")

"""
    Creazione del file di intersezione degli studenti
"""
for file in os.listdir(OUTPUT_PATH_ID_INC):
    if not file.endswith('.xls') and not file.split('.')[0].isnumeric():
        continue
    id_inc = file.split('.')[0]
    set_matricole = set()
    xls = pd.read_excel(f"{OUTPUT_PATH_ID_INC}/{file}")
    res = pd.DataFrame(filter(lambda val: str(val[-1]).endswith('23') or str(val[-1]).startswith("Da frequentare") , xls.to_numpy()))
    if len(res) == 0:
        extractor_log.write(f'IL FILE {file} non ha prodotto risultati\n')
        continue
    res.columns = xls.columns
    #print(xls.to_numpy())
    #xls = xls[xls['DEBITO'] == 'Frequentato nel 2022/2023']

    set_matricole = set(res['MATRICOLA'].unique())
    if id_inc not in mapIdIncToSetMatricole:
        mapIdIncToSetMatricole[id_inc] = set_matricole
    else:
        extractor_log(f'ERRORE ID_INC DUPLICATO FILE {file}\n')

print(len(mapIdIncToSetMatricole))
list_keys = list(mapIdIncToSetMatricole)
workbook = xlsxwriter.Workbook(INTERESEZIONE_STUDENTI)
ws = workbook.add_worksheet()
ws.write(0,0, 'Insegnamento1')
ws.write(0,1, 'Insegnamento2')
ws.write(0,2, 'N Studenti Intersezione')
ws.write(0,3, 'Intersezione1 (Percentuale degli studenti di Insegnamento1 che seguono anche Insegnamento2)')
ws.write(0,4, 'Intersezione2 (Percentuale degli studenti di Insegnamento2 che seguono anche Insegnamento1)')
offset = 1
for key1 in list_keys:
    #ws.write(0,i+1,key1)
    #ws.write(i+1,0,key1)
    for key2 in list_keys:
        if key1 >= key2:
            continue
        set1 = mapIdIncToSetMatricole[key1]
        set2 = mapIdIncToSetMatricole[key2]
        if(not set1 or not set2):
            extractor_log.write(f'''------------------------------------
[{key1}] n matricole = [{len(set1)}]
[{key2}] n matricole = [{len(set2)}]
------------------------------------''')
            continue
        intersenzione = set.intersection(set1, set2)
        val1 = round(len(intersenzione)/len(set1)*100)
        val2 = round(len(intersenzione)/len(set2)*100)
        if(len(intersenzione) > 0):
            ws.write(offset, 0, int(key1))
            ws.write(offset, 1, int(key2))
            ws.write(offset, 2, len(intersenzione))
            ws.write(offset, 3, val1)
            ws.write(offset, 4, val2)
            offset+=1
        if(len(intersenzione) > 200):
           print(key1, key2, len(set1), len(set2), len(intersenzione), val1, val2)



workbook.close()
extractor_log.close()

xls_gof = pd.read_excel(FILE_GOF)

distinct_id_inc = {str(row[14]) for row in xls_gof.values}
print(f"Dal file del GOF risultano presenti {len(distinct_id_inc)} id_inc univoci")

diff = set.difference(distinct_id_inc, set(mapIdIncToSetMatricole.keys()))
print(f"Risultano {len(diff)} id_inc mancanti")
ins_mancanti = list(filter(lambda row: str(row[14]) in diff, xls_gof.values))

workbook = xlsxwriter.Workbook(f'{BASE_PATH}/ins_mancanti.xlsx')
worksheet = workbook.add_worksheet()
for i, col in enumerate(list(xls_gof.columns)):
    worksheet.write(0, i, col)
for r in range(len(ins_mancanti)):
    for c in range(len(list(xls_gof.columns))):
        worksheet.write(r+1, c, ins_mancanti[r][c] if type(ins_mancanti[r][c]) != float else 'N')
workbook.close()

  

