import os, shutil
import pandas as pd
from Costanti import *

#FILE_GOF = "Dati_insegnamenti_final.xlsx"

xls_gof = pd.read_excel(FILE_GOF)

"""
results = filter(lambda row: row[6] == cod_ins and first_cognome[:3] >= row[15].split('-')[0] and first_cognome[:3] <= row[15].split('-')[1], xls.values)
for row in results:
    print(row[6], row[12])
"""
fileNonPresentidir = PATH_FILE_NON_PRESENTI
filePiuIDINCdir = PATH_FILE_PIU_ID_INC

fileCorrettidir = OUTPUT_PATH_ID_INC

if not os.path.isdir(fileNonPresentidir):
    os.mkdir(fileNonPresentidir)
if not os.path.isdir(filePiuIDINCdir):
    os.mkdir(filePiuIDINCdir)

log_file = open(f'{LOG_PATH}/logs.txt', 'w', encoding="utf-8")
for file in os.listdir(INPUT_PATH_XLSX):
    if not file.endswith('.xlsx') or file == FILE_GOF:
        continue
    if file.split('.')[0].isnumeric():
        continue
    if not file.split('_')[-1].startswith('2023'):
        continue
    new_xls = pd.read_excel(f"{INPUT_PATH_XLSX}/{file}")
    try:
        list_cod_ins = {x[3].split(' ')[0] for x in new_xls.values}
    except IndexError:
        log_file.write(f'ERRORE CON FILE {file}')
    #cod_ins = list_cod_ins[0]
    try:
        cognome = new_xls.values[0][1][:3]
    except Exception as e:
        log_file.write(f'ERRORE {e}\n PER IL FILE {file}')
    results = list(filter(lambda row: row[6] in list_cod_ins and cognome >= row[13].split('-')[0] and cognome <= row[13].split('-')[1], xls_gof.values))
    if(not results):
        try:
            os.rename(f"{INPUT_PATH_XLSX}/{file}", f'{fileNonPresentidir}/{file}')
            log_file.write(f'ERRORE IL FILE {file} NON E STATO TROVATO NEL FILE DEL GOF\n')
        except FileExistsError:
            log_file.write(f'IL FILE {file} VIENE SPOSTATO MA NON DOVREBBE\n')
        continue
    id_inc = {r[14] for r in results}
    if(len(id_inc) > 1):
        log_file.write(f'ERRORE IL FILE {file} NELLA RICERCA HA PRODOTTO PIU ID_INC\n')
        for id in id_inc:
            try:
                new_file = f'{str(id)}.xlsx'
                shutil.copy(f"{INPUT_PATH_XLSX}/{file}", f"{fileCorrettidir}/{new_file}")
            except FileExistsError:
                log_file.write(f'ERRORE IL FILE [{new_file}] ESISTE GIA E NON PUO ESSERE CREATO A PARTIRE DA [{file}]')
        os.rename(f"{INPUT_PATH_XLSX}/{file}", f'{filePiuIDINCdir}/{file}')   
        continue
    try:
        new_file = f'{str(id_inc.pop())}.xlsx'
        os.rename(f"{INPUT_PATH_XLSX}/{file}", f"{fileCorrettidir}/{new_file}")
    except FileExistsError as e: 
        log_file.write(f'ERRORE {e.strerror} PER IL FILE {file}\n')
        other_xls = pd.read_excel(f"{OUTPUT_PATH_ID_INC}/{new_file}")
        other_cognome = other_xls.values[0][1][:3]
        if(other_cognome == cognome):
            log_file.write(f'FILE DUPLICATO TROVATO ELIMINO... {file} IN FAVORE DI {new_file}\n')
            os.remove(f"{INPUT_PATH_XLSX}/{file}")

distinct_id_inc = {row[14] for row in xls_gof.values}
print(len(distinct_id_inc))
log_file.close()

