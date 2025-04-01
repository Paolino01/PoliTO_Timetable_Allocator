import os
import xml.dom.minidom, xml.etree.ElementTree as et
import pandas as pd
from dbAPI import dbAPI
import shutil


"""
    Script utilizzato per aggiornare l'id_inc dei file sugli studenti iscritti agli insegnamenti,
    passando da 22/23 a 23/24
"""
file_gof = "C:/Users/manue/Desktop/allocatore_orario_polito_2223/20230509_Ins_2024_ICM_ETF_OdC x orari.xlsx"
xls_gof = pd.read_excel(file_gof)

db:dbAPI = dbAPI("C:/Users/manue/Desktop/NEW2.db")


path = "id_xmls"
with open('update_id_log.txt', 'w') as log:
    for file in os.listdir(path):
        print(file)
        id_inc = file.split(".")[0]
        cod_insList = db.get_CodInsInsegnamento(id_inc)
        if(cod_insList):
            for cod_ins in cod_insList:
                ins_row = xls_gof[xls_gof['COD_INS'] == cod_ins[0]]
                if len(ins_row) > 0:
                    break
            if(len(ins_row) < 1):
                log.write(f"ROW NON TROVATA per ins [{id_inc}]\n")
                continue
            id_insList = sorted(set(ins_row['ID_INC']))#
            new_path = 'new_id_ins'
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            
            for id in id_insList:
                if(not os.path.exists(f"{new_path}/{id}.xlsx")):
                    shutil.copy(f"{path}/{file}", f"{new_path}/{id}.xlsx")
                    print("done")
                    break
            

        else:
            log.write(f"{id_inc} Non trovato nel db\n")