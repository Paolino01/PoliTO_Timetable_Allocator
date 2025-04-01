# import xml.etree.ElementTree as et
# import xlsxwriter
# import numpy as np
# import os , json, sys
# import pandas as pd
# from constantsScraper import *
# from auxExtractor import *

# def __main__():

#     def add_ins_to_list(semestre, ins):
#         if(semestre == '1'):
#             insegnamenti_1_semestre.append(ins)
#         else:
#             insegnamenti_2_semestre.append(ins)
#         return

#     def media(n1, n2):
#         return str((n1 + n2) // 2)

#     def fill_matrice(insegnamenti:list[Insegnamento], lato, info_correlazioni):
#         size = lato**2
#         matrice = np.array([None]*(size)).reshape(lato,lato)
#         for i in range(2, lato):
#             cod_ins = insegnamenti[i-2].codice
#             nome_ins = insegnamenti[i-2].nome
#             matrice[0][i] = nome_ins
#             matrice[1][i] = cod_ins
#             matrice[i][0] = nome_ins
#             matrice[i][1] = cod_ins
#             matrice[i][i] = 0
#             for k in range(i+1, lato):
#                 cod_ins2 = insegnamenti[k-2].codice    
#                 try:
#                     matrice[k][i] = info_correlazioni[cod_ins][cod_ins2]
#                 except KeyError:
#                     try:
#                         matrice[k][i] = info_correlazioni[cod_ins2][cod_ins]
#                     except KeyError:
#                         matrice[k][i] = '0'
#         return matrice

#     def insert_info_in_excel(lato, matrice, nome_file):
#         workbook = xlsxwriter.Workbook(path+nome_file)
#         worksheet = workbook.add_worksheet()
#         bold = workbook.add_format({'bold': True})
#         for i in range(lato):
#             for k in range(lato):
#                 if(matrice[i][k] != None):
#                     if(i in range(2) or k in range(2)):
#                         worksheet.write(i, k, matrice[i][k], bold)
#                     else:
#                         worksheet.write(i, k, float(matrice[i][k]))
#         workbook.close()

#     def generate_all_correlazioni(semestre):
#         correlazione_all_orientamenti = {}
#         for nome_orientamento in all_info_correlazione[semestre]:
#             orientamento = all_info_correlazione[semestre][nome_orientamento]
#             for cod_ins, cod_ins_list in orientamento.items():
#                 for cod_ins2, corr in cod_ins_list.items():
#                     if cod_ins == cod_ins2:
#                         continue
#                     keys = list(correlazione_all_orientamenti.keys())
#                     inner_keys1 = list(correlazione_all_orientamenti[cod_ins].keys()) if cod_ins in keys else []
#                     inner_keys2 = list(correlazione_all_orientamenti[cod_ins2].keys()) if cod_ins2 in keys else []

#                     #No chiavi precedenti -> creazione record
#                     if not (inner_keys1 or inner_keys2):
#                         correlazione_all_orientamenti[cod_ins] = {cod_ins2: [corr]}
#                     #Record esistente -> Aggiungo alla lista la correlazione
#                     elif cod_ins2 in inner_keys1 : 
#                         correlazione_all_orientamenti[cod_ins][cod_ins2].append(corr)
#                     elif cod_ins in inner_keys2:
#                         correlazione_all_orientamenti[cod_ins2][cod_ins].append(corr)
#                     #Esiste gia una delle due chiavi, ma non la coppia -> Creo la coppia
#                     elif inner_keys1:
#                         correlazione_all_orientamenti[cod_ins][cod_ins2] = [corr]
#                     elif inner_keys2:
#                         correlazione_all_orientamenti[cod_ins2][cod_ins] = [corr]
#                     else:
#                         print("Error", file=sys.stderr)                    
        
#         #Riduco le correlazioni delle coppie ad un valore singolo
#         for cod_ins, val in correlazione_all_orientamenti.items():
#             for cod_ins2, corr_list in val.items():
#                 corr_list = list(map(lambda corr: float(corr), corr_list))
#                 #Si potrebbe scegliere di usare una funzione diversa da Max, se si volesse avere un incremento
#                 #sulla base del numero di volte che la coppia si presenta (i.e. la coppia esiste in piu orientamenti)
#                 correlazione_all_orientamenti[cod_ins][cod_ins2] = str(max(corr_list))

#         return correlazione_all_orientamenti

#     def get_insegnamenti_obbligatori(insegnamenti_xml) -> list[Insegnamento]:
#         return [Insegnamento(semestre,x.text,x.attrib.get(NOME_STRING), '100', -1) for x in insegnamenti_xml]

#     def get_insegnamenti_obbligatori_lingua(insegnamenti_scelta_lingua_xml) -> tuple[list[Insegnamento],list[Insegnamento]]:
#         ins_eng = []
#         ins_ita = []
#         for lista_opzioni in insegnamenti_scelta_lingua_xml:
#             foundEn = False
#             for ins in lista_opzioni.findall(OPZIONE_STRING):
#                 # Fix orribile per gli insegnamenti in Oppure ma stessa lingua
#                 if(ins.attrib.get(PREFERITO_XML) and not foundEn):
#                     ins_eng.append(Insegnamento(semestre, ins.text, ins.attrib.get(NOME_STRING), '', -1))
#                     foundEn = True
#                 else:
#                     ins_ita.append(Insegnamento(semestre, ins.text, ins.attrib.get(NOME_STRING), '', -1))
#         return (list(ins_eng), list(ins_ita))

#     def get_tabelle_scelta(tabelle_scelta_xml, anno) -> list[Tabella]:
#         lista_tabelle = []
#         for x in tabelle_scelta_xml:
#             new_tab = Tabella(x.attrib.get(NOME_TABELLA_STRING), anno, x.attrib.get(CREDITI_STRING))
#             lista_ins = [Insegnamento(
#                 semestre,
#                 ins.text,
#                 ins.attrib.get(NOME_STRING),
#                 ins.attrib.get(CORRELAZIONE_STRING),
#                 ins.attrib.get(CREDITI_STRING),
#             ) for ins in x.findall(OPZIONE_STRING)]
#             new_tab.set_lista_insegnamenti(lista_ins)
#             lista_tabelle.append(new_tab)
#         return lista_tabelle

#     def get_tabelle_annuali(tabelle_annuali_xml, anno, semestre) -> list[Tabella]:
#         if(not tabelle_annuali_xml):
#             return []
#         lista_tabelle = []
#         for tabella_lingua_xml in tabelle_annuali_xml.findall(NOME_TABELLA_LINGUA_XML):
#             tab = Tabella(tabella_lingua_xml.get(NOME_TABELLA_STRING), anno, '-1')
#             tab.set_lista_insegnamenti([Insegnamento(semestre, ins_xml.text, ins_xml.attrib.get(NOME_STRING), '100', -1) for ins_xml in tabella_lingua_xml.findall(INSEGNAMENTO_STRING)])
#             lista_tabelle.append(tab)
#         return lista_tabelle

#     def get_scelta_tabelle_scelta(scelta_tabelle_scelta_xml, anno, semestre) -> list[Tabella]:
#         if(not scelta_tabelle_scelta_xml):
#             return []
#         lista_tabelle = []
#         for tabella_lingua_xml in scelta_tabelle_scelta_xml.findall(NOME_SCELTA_TABELLA_XML):
#             tab = Tabella(tabella_lingua_xml.get(NOME_TABELLA_STRING), anno, tabella_lingua_xml.get(CREDITI_STRING))
#             tab.set_lista_insegnamenti([Insegnamento(semestre, ins_xml.text, ins_xml.attrib.get(NOME_STRING), ins_xml.attrib.get(CORRELAZIONE_STRING), ins_xml.attrib.get(CREDITI_STRING)) for ins_xml in tabella_lingua_xml.findall(OPZIONE_STRING)])
#             lista_tabelle.append(tab)
#         return lista_tabelle


#     if(not os.path.isdir(BASE_PATH_FILE_EXCEL)):
#         os.mkdir(BASE_PATH_FILE_EXCEL)

#     for file in os.listdir(BASE_PATH_FILE_XML):
#         content = et.parse(f"{BASE_PATH_FILE_XML}/{file}") 
#         cdl = content.getroot()

#         cdl_name = cdl.attrib.get(NOME_STRING)
#         cdl_name = cdl_name.replace('  ', ' ').replace('  ', ' ').replace('/', '_')
#         cdl_name = cdl_name[9 : cdl_name.find(')')+1]
#         if not os.path.exists(f"{BASE_PATH_FILE_EXCEL}/{cdl_name}"):
#             os.makedirs(f"{BASE_PATH_FILE_EXCEL}/{cdl_name}")

#         all_info_correlazione = {'Semestre1': {}, 'Semestre2': {}}
#         ins_all_orientamenti_sem1 = []
#         ins_all_orientamenti_sem2 = []

#         for orientamento in cdl:
#             path = f"{BASE_PATH_FILE_EXCEL}/{cdl_name}/"
#             orientamento_name = orientamento.attrib.get(NOME_STRING)
#             orientamento_name = orientamento_name.replace('"',"")
#             if not os.path.exists(path+orientamento_name.replace('/','_')):
#                 try:
#                     os.makedirs(path+orientamento_name)
#                 except:
#                     print(f"Impossibile creare orientamento {orientamento_name}", cdl_name)
#                     continue
#             path = path+orientamento_name+'/'

#             insegnamenti_1_semestre = []
#             insegnamenti_2_semestre = []
#             info_correlazioni = {}

#             for periodo in orientamento:
#                 anno = periodo.find(ANNO_STRING).text
#                 semestre = periodo.find(SEMESTRE_STRING).text
#                 lista_ins_xml = periodo.find(NOME_LISTA_INSEGNAMENTI_XML)

#                 ins_obbligatori:list[Insegnamento] = get_insegnamenti_obbligatori(lista_ins_xml.findall(INSEGNAMENTO_STRING))

#                 ins_obbligatori_eng, ins_obbligatori_ita = get_insegnamenti_obbligatori_lingua(lista_ins_xml.findall(NOME_SCELTA_LINGUA_XML))

#                 tabelle_ins_scelta: list[Tabella] = get_tabelle_scelta(lista_ins_xml.findall(NOME_SCELTA_TABELLA_XML), anno)

#                 tabelle_annuali: list[Tabella] = get_tabelle_annuali(lista_ins_xml.find(NOME_SCELTA_TABELLA_LINGUA_XML), anno, semestre)

#                 scelta_tabelle_scelta: list[Tabella] = get_scelta_tabelle_scelta(lista_ins_xml.find(NOME_SCELTA_TABELLA_SCELTA_XML), anno, semestre)

#                 ind_crediti = -1
#                 other_tab_ind = []
#                 for ind, tab in enumerate(tabelle_ins_scelta):
#                     if(any(nome in tab.nome for nome in NOME_TABELLE_CON_CREDITI_LIBERI)):
#                         ind_crediti = ind
#                     else:
#                         other_tab_ind.append(ind)
#                 if(ind_crediti != -1 and other_tab_ind):
#                     for i in other_tab_ind:
#                         tabelle_ins_scelta[ind_crediti].rimuovi_insegnamenti(tabelle_ins_scelta[i].get_lista_insegnamenti())
                

#                 ####### Calcolo info correlazioni #######
#                 for index, ins in enumerate(ins_obbligatori):
#                     if(ins.codice not in info_correlazioni.keys()):
#                         add_ins_to_list(semestre, ins)
#                         info_correlazioni[ins.codice] = {}
#                     for k in range(index+1, len(ins_obbligatori)):
#                         info_correlazioni[ins.codice][ins_obbligatori[k].codice] = MAX_CORRELAZIONE
#                     for ins_eng in ins_obbligatori_eng:
#                         info_correlazioni[ins.codice][ins_eng.codice] = MAX_CORRELAZIONE
#                     for ins_ita in ins_obbligatori_ita:
#                         info_correlazioni[ins.codice][ins_ita.codice] = MAX_CORRELAZIONE
#                     if(tabelle_ins_scelta):
#                         for tab in tabelle_ins_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione
#                     if(scelta_tabelle_scelta):
#                         for tab in scelta_tabelle_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione

#                 for tabella in tabelle_annuali:
#                     lista_ins = tabella.get_lista_insegnamenti()
#                     for ind_ins, ins in enumerate(lista_ins):
#                         if(ins.codice not in info_correlazioni.keys()):
#                             add_ins_to_list(semestre, ins)
#                             info_correlazioni[ins.codice] = {}
#                         for k in range(ind_ins+1, len(lista_ins)):
#                             info_correlazioni[ins.codice][lista_ins[k].codice] = MAX_CORRELAZIONE
#                         for i in range(len(ins_obbligatori_eng)):
#                             info_correlazioni[ins.codice][ins_obbligatori_eng[i].codice] = MAX_CORRELAZIONE
#                             info_correlazioni[ins.codice][ins_obbligatori_ita[i].codice] = CORRELAZIONE_OBBLIGATORI_LINGUE_DIVERSE
#                         if(tabelle_ins_scelta):
#                             for tab in tabelle_ins_scelta:
#                                 for ins_tab in tab.get_lista_insegnamenti():
#                                     info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione
#                         if(scelta_tabelle_scelta):
#                             for tab in scelta_tabelle_scelta:
#                                 for ins_tab in tab.get_lista_insegnamenti():
#                                     info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione


#                 for index, ins in enumerate(ins_obbligatori_eng):
#                     if(ins.codice not in info_correlazioni.keys()):
#                         add_ins_to_list(semestre, ins)
#                         info_correlazioni[ins.codice] = {}
#                     for k in range(index+1, len(ins_obbligatori_eng)):
#                         info_correlazioni[ins.codice][ins_obbligatori_eng[k].codice] = MAX_CORRELAZIONE
#                     for i in range(len(ins_obbligatori_ita)):
#                         if(i != index):
#                             info_correlazioni[ins.codice][ins_obbligatori_ita[i].codice] = CORRELAZIONE_OBBLIGATORI_LINGUE_DIVERSE
#                         else:
#                             info_correlazioni[ins.codice][ins_obbligatori_ita[i].codice] = '0'
#                     if(tabelle_ins_scelta):
#                         for tab in tabelle_ins_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione
#                     if(scelta_tabelle_scelta):
#                         for tab in scelta_tabelle_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione

#                 for index, ins in enumerate(ins_obbligatori_ita):
#                     if(ins.codice not in info_correlazioni.keys()):
#                         add_ins_to_list(semestre, ins)
#                         info_correlazioni[ins.codice] = {}
#                     for k in range(index+1, len(ins_obbligatori_ita)):
#                         info_correlazioni[ins.codice][ins_obbligatori_ita[k].codice] = MAX_CORRELAZIONE
#                     if(tabelle_ins_scelta):
#                         for tab in tabelle_ins_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione
#                     if(scelta_tabelle_scelta):
#                         for tab in scelta_tabelle_scelta:
#                             for ins_tab in tab.get_lista_insegnamenti():
#                                 info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione

#                 if(tabelle_ins_scelta):            
#                     for n_ind, indice in enumerate(other_tab_ind):
#                         ins_list:list[Insegnamento] = tabelle_ins_scelta[indice].get_lista_insegnamenti()
#                         for ins in ins_list:
#                             if(ins.codice not in info_correlazioni.keys()):
#                                 add_ins_to_list(semestre, ins)
#                                 info_correlazioni[ins.codice] = {}
#                             for k in range(n_ind+1, len(other_tab_ind)):
#                                 ins_list2 = tabelle_ins_scelta[k].get_lista_insegnamenti()
#                                 for ins2 in ins_list2:
#                                     info_correlazioni[ins.codice][ins2.codice] = media(int(ins.correlazione), int(ins2.correlazione))
#                             if(ind_crediti != -1):
#                                 for ins_crediti_liberi in tabelle_ins_scelta[ind_crediti].get_lista_insegnamenti():
#                                     info_correlazioni[ins.codice][ins_crediti_liberi.codice] = ins_crediti_liberi.correlazione
#                             if(scelta_tabelle_scelta):
#                                 for tab in scelta_tabelle_scelta:
#                                     for ins_tab in tab.get_lista_insegnamenti():
#                                         info_correlazioni[ins.codice][ins_tab.codice] = ins_tab.correlazione
#                     if(ind_crediti != -1):
#                         min_crediti = tabelle_ins_scelta[ind_crediti].crediti
#                         lista_ins = tabelle_ins_scelta[ind_crediti].get_lista_insegnamenti()
#                         for ind, ins in enumerate(lista_ins):
#                             crediti = ins.crediti
#                             if(ins.codice not in info_correlazioni.keys()):
#                                 add_ins_to_list(semestre, ins)
#                                 info_correlazioni[ins.codice] = {}
#                             if(crediti < min_crediti):
#                                 for k in range(ind+1, len(lista_ins)):
#                                     crediti_2 = lista_ins[k].crediti
#                                     ins2 = lista_ins[k]
#                                     if(crediti_2 < min_crediti):
#                                         info_correlazioni[ins.codice][ins2.codice] = media(int(ins.correlazione), int(ins2.correlazione))
#                                     if(crediti + crediti_2 < min_crediti):
#                                         print('CASO PARTICOLARE CREDITI')

#                 if(scelta_tabelle_scelta):
#                     for tab in scelta_tabelle_scelta:
#                         min_crediti = tab.crediti
#                         lista_ins:list[Insegnamento] = tab.get_lista_insegnamenti()
#                         for ind, ins in enumerate(lista_ins):
#                             crediti = ins.crediti
#                             if(ins.codice not in info_correlazioni.keys()):
#                                 add_ins_to_list(semestre, ins)
#                                 info_correlazioni[ins.codice] = {}
#                             if(crediti < min_crediti):
#                                 for k in range(ind+1, len(lista_ins)):
#                                     crediti_2 = lista_ins[k].crediti
#                                     ins2 = lista_ins[k]
#                                     if(crediti_2 < min_crediti):
#                                         info_correlazioni[ins.codice][ins2.codice] = media(int(ins.correlazione), int(ins2.correlazione))
#                                     if(crediti + crediti_2 < min_crediti):
#                                         print('CASO PARTICOLARE CREDITI', cdl_name, orientamento_name, anno, semestre)
                                
            
#                         ####### Fine calcolo info correlazioni ########

#             if (orientamento_name not in all_info_correlazione['Semestre1'].keys()):
#                 test = {
#                     k: v
#                     for k, v in info_correlazioni.items()
#                     if k in [ins.codice for ins in insegnamenti_1_semestre]
#                 }
#                 all_info_correlazione['Semestre1'][orientamento_name] = test
#             if (orientamento_name not in all_info_correlazione['Semestre2'].keys()):
#                 test = {
#                     k: v
#                     for k, v in info_correlazioni.items()
#                     if k in [ins.codice for ins in insegnamenti_2_semestre]
#                 }
#                 all_info_correlazione['Semestre2'][orientamento_name] = test

#             len_matrice_1 = len(insegnamenti_1_semestre) + 2
#             matrice_1_semestre = fill_matrice(insegnamenti_1_semestre, len_matrice_1, info_correlazioni)
            
#             len_matrice_2 = len(insegnamenti_2_semestre) + 2
#             matrice_2_semestre = fill_matrice(insegnamenti_2_semestre, len_matrice_2, info_correlazioni)

#             insert_info_in_excel(len_matrice_1, matrice_1_semestre, f"{orientamento_name}_semestre1.xlsx")
#             insert_info_in_excel(len_matrice_2, matrice_2_semestre,  f"{orientamento_name}_semestre2.xlsx")

#             ins_all_orientamenti_sem1 += insegnamenti_1_semestre
#             ins_all_orientamenti_sem2 += insegnamenti_2_semestre

#         path = f"{BASE_PATH_FILE_EXCEL}/{cdl_name}/"
#         correlazione_all_orientamenti_sem1 = generate_all_correlazioni('Semestre1')
#         ins_all_orientamenti_sem1 = sorted(list(set(ins_all_orientamenti_sem1)))
#         lato = len(ins_all_orientamenti_sem1) + 2
#         matrice_all_1_semestre = fill_matrice(ins_all_orientamenti_sem1, lato, correlazione_all_orientamenti_sem1)
#         insert_info_in_excel(lato, matrice_all_1_semestre, f"{cdl_name.split(' (')[0]}_semestre1.xlsx")

#         correlazione_all_orientamenti_sem2 = generate_all_correlazioni('Semestre2')
#         ins_all_orientamenti_sem2 = sorted(list(set(ins_all_orientamenti_sem2)))
#         lato = len(ins_all_orientamenti_sem2) + 2
#         matrice_all_2_semestre = fill_matrice(ins_all_orientamenti_sem2, lato, correlazione_all_orientamenti_sem2)
#         insert_info_in_excel(lato, matrice_all_2_semestre, f"{cdl_name.split(' (')[0]}_semestre2.xlsx")

# def generateCdlExcel(menuVersion):
#     log = open("generateCdlExcel_log.txt", "w", encoding="utf-8")
#     menuVersion = menuVersion
#     if menuVersion:
#         while True:
#             counter = 0
#             path = input("Inserire Percorso file excel modificati: ")
#             if os.path.isdir(path):
#                 break
#             elif counter > 5:
#                 exit()
#             counter += 1
#         while True:
#             counter = 0
#             sem = input("Inserire semestre da considerare ")
#             if sem in ["1","2"]:
#                 semestre = f"semestre{sem}"
#                 break
#             elif counter > 5:
#                 exit()
#             counter += 1 
#     else:
#         path = BASE_PATH_FILE_EXCEL
#         semestre = SEMESTRE_STRING + SEMESTRE
#     for dir in os.listdir(path):
#         log.write(f"INSIDE dir {dir}\n")
#         currPath = f"{path}/{dir}"
#         insDict = {}
#         insNameList = [] 
#         for orientamento in os.listdir(currPath):
#             currPath = f"{path}/{dir}/{orientamento}"
#             if os.path.isdir(currPath):
#                 log.write(f"\tORIENTAMENTO {orientamento}\n")
#                 for file in os.listdir(currPath):
#                     if(not file.endswith(f"{semestre}.xlsx")):
#                         continue
#                     log.write(f"LEGGO FILE {file}:\n")
#                     xls = pd.read_excel(f"{currPath}/{file}", header=None)
#                     xlsMatrix = xls.to_numpy()
#                     for row in range(2, len(xlsMatrix)-1):
#                         t1 = (xlsMatrix[row][0],xlsMatrix[row][1])
#                         insNameList.append(t1)
#                         for row2 in range(row+1, len(xlsMatrix)):
#                             t2 = (xlsMatrix[row2][0],xlsMatrix[row2][1])

#                             if t1 == t2:
#                                 continue
#                             keys = list(insDict.keys())
#                             inner_keys1 = list(insDict[t1].keys()) if t1 in keys else []
#                             inner_keys2 = list(insDict[t2].keys()) if t2 in keys else []
#                             corr = xlsMatrix[row2,row]
#                             if(corr == 0):
#                                 continue

#                             if not (inner_keys1 or inner_keys2):
#                                 insDict[t1] = {t2: [corr]}
#                             elif t2 in inner_keys1 : 
#                                 insDict[t1][t2].append(corr)
#                             elif t1 in inner_keys2:
#                                 insDict[t2][t1].append(corr)
#                             elif inner_keys1:
#                                 insDict[t1][t2] = [corr]
#                             elif inner_keys2:
#                                 insDict[t2][t1] = [corr]
#                             else:
#                                 print("Error", file=sys.stderr)
                            
#         for t1, val in insDict.items():
#             for t2, corr_list in val.items():
#                 corr_list = list(map(lambda corr: float(corr), corr_list))
#                 insDict[t1][t2] = str(max(corr_list))

#         insNameList = sorted(list(set(insNameList)))
#         lato = len(insNameList) + 2
#         matrice_all_1_semestre = fill_matrice(insNameList, lato, insDict)
#         insert_info_in_excel(lato, matrice_all_1_semestre, f"{dir}_{semestre}.xlsx")                   

#         #print(insDict)
#     log.close()

# def fill_matrice(insegnamenti, lato, info_correlazioni):
#         size = lato**2
#         matrice = np.array([None]*(size)).reshape(lato,lato)
#         for i in range(2, lato):
#             nome_ins = insegnamenti[i-2][0]
#             cod_ins = insegnamenti[i-2][1]
#             matrice[0][i] = nome_ins
#             matrice[1][i] = cod_ins
#             matrice[i][0] = nome_ins
#             matrice[i][1] = cod_ins
#             matrice[i][i] = 0
#             for k in range(i+1, lato):
#                 cod_ins2 = insegnamenti[k-2][1]    
#                 try:
#                     matrice[k][i] = info_correlazioni[insegnamenti[i-2]][insegnamenti[k-2]]
#                 except KeyError:
#                     try:
#                         matrice[k][i] = info_correlazioni[insegnamenti[k-2]][insegnamenti[i-2]]
#                     except KeyError:
#                         matrice[k][i] = '0'
#         return matrice

# def insert_info_in_excel(lato, matrice, nome_file):
#     path = BASE_PATH_FILE_RESULT_XML
    
#     sub_path = path.split("/")
#     actual_path = "./"

#     for path in sub_path:
#         actual_path += path + "/"
#         if not os.path.isdir(actual_path):
#             os.mkdir(actual_path)

#     workbook = xlsxwriter.Workbook(actual_path+nome_file)
#     worksheet = workbook.add_worksheet()
#     bold = workbook.add_format({'bold': True})
#     for i in range(lato):
#         for k in range(lato):
#             if(matrice[i][k] != None):
#                 if(i in range(2) or k in range(2)):
#                     worksheet.write(i, k, matrice[i][k], bold)
#                 else:
#                     worksheet.write(i, k, float(matrice[i][k]))
#     workbook.close()


import xml.etree.ElementTree as ET
import xlsxwriter
import numpy as np
import os, json, sys
import pandas as pd
from constantsScraper import *
from auxExtractor import *

# Main function
def __main__():

    # Function to add a course to the corresponding semester list
    def add_course_to_list(semester, course):
        if semester == '1':
            courses_semester_1.append(course)  # Add to the first semester list
        else:
            courses_semester_2.append(course)  # Add to the second semester list
        return

    # Function to compute the integer average of two values
    def calculate_average(n1, n2):
        return str((n1 + n2) // 2)

    # Function to create and populate a correlation matrix
    def populate_correlation_matrix(courses: list[Course], size, correlation_data):
        matrix = np.array([None] * (size ** 2)).reshape(size, size)

        # Fill the matrix with course names and codes
        for i in range(2, size):
            course_code = courses[i - 2].code
            course_name = courses[i - 2].name
            matrix[0][i] = course_name
            matrix[1][i] = course_code
            matrix[i][0] = course_name
            matrix[i][1] = course_code
            matrix[i][i] = 0  # Self-correlation (0)

            # Populate correlation values between courses
            for k in range(i + 1, size):
                course_code_2 = courses[k - 2].code
                try:
                    matrix[k][i] = correlation_data[course_code][course_code_2]
                except KeyError:
                    try:
                        matrix[k][i] = correlation_data[course_code_2][course_code]
                    except KeyError:
                        matrix[k][i] = '0'  # Default for missing correlation
        return matrix

    # Function to save the correlation matrix into an Excel file
    def save_to_excel(size, matrix, file_name):
        workbook = xlsxwriter.Workbook(output_path + file_name)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        # Iterate through the matrix and write values to the Excel sheet
        for i in range(size):
            for k in range(size):
                if matrix[i][k] is not None:
                    if i < 2 or k < 2:
                        worksheet.write(i, k, matrix[i][k], bold)
                    else:
                        worksheet.write(i, k, float(matrix[i][k]))
        workbook.close()

    # Function to generate correlation data for all specializations in a semester
    def generate_all_correlations(semester):
        all_specialization_correlations = {}

        # Process correlations between courses in each specialization
        for specialization_name in all_correlation_data[semester]:
            specialization = all_correlation_data[semester][specialization_name]

            for course_code, correlated_courses in specialization.items():
                for course_code_2, correlation in correlated_courses.items():
                    if course_code == course_code_2:
                        continue
                    existing_keys = list(all_specialization_correlations.keys())
                    existing_subkeys_1 = list(all_specialization_correlations[course_code].keys()) if course_code in existing_keys else []
                    existing_subkeys_2 = list(all_specialization_correlations[course_code_2].keys()) if course_code_2 in existing_keys else []

                    # Create a new correlation entry if none exists
                    if not (existing_subkeys_1 or existing_subkeys_2):
                        all_specialization_correlations[course_code] = {course_code_2: [correlation]}
                    # Append correlation value to an existing record
                    elif course_code_2 in existing_subkeys_1:
                        all_specialization_correlations[course_code][course_code_2].append(correlation)
                    elif course_code in existing_subkeys_2:
                        all_specialization_correlations[course_code_2][course_code].append(correlation)
                    # If one key exists, create the pair
                    elif existing_subkeys_1:
                        all_specialization_correlations[course_code][course_code_2] = [correlation]
                    elif existing_subkeys_2:
                        all_specialization_correlations[course_code_2][course_code] = [correlation]
                    else:
                        print("Error", file=sys.stderr)

        # Store only the maximum correlation value for each pair
        for course_code, correlations in all_specialization_correlations.items():
            for course_code_2, correlation_list in correlations.items():
                correlation_list = list(map(float, correlation_list))
                all_specialization_correlations[course_code][course_code_2] = str(max(correlation_list))

        return all_specialization_correlations

    # Function to get mandatory courses from XML
    def get_mandatory_courses(course_list_xml) -> list[Course]:
        return [Course(semester, x.text, x.attrib.get(COURSE_NAME_STRING), '100', -1) for x in course_list_xml]

    # Function to get mandatory courses based on language (English/Italian)
    def get_language_specific_courses(language_course_selection_xml) -> tuple[list[Course], list[Course]]:
        english_courses = []
        italian_courses = []
        for option_list in language_course_selection_xml:
            found_english = False
            for course in option_list.findall(OPTION_STRING):
                # Avoid duplicate language course selection
                if course.attrib.get(PREFERRED_LANGUAGE_XML) and not found_english:
                    english_courses.append(Course(semester, course.text, course.attrib.get(COURSE_NAME_STRING), '', -1))
                    found_english = True
                else:
                    italian_courses.append(Course(semester, course.text, course.attrib.get(COURSE_NAME_STRING), '', -1))
        return english_courses, italian_courses

    # Function to get elective course tables from XML
    def get_elective_course_tables(elective_tables_xml, year) -> list[Table]:
        table_list = []
        for x in elective_tables_xml:
            new_table = Table(x.attrib.get(TABLE_NAME_STRING), year, x.attrib.get(CREDITS_STRING))
            course_list = [
                Course(
                    semester,
                    course.text,
                    course.attrib.get(COURSE_NAME_STRING),
                    course.attrib.get(CORRELATION_STRING),
                    course.attrib.get(CREDITS_STRING),
                ) for course in x.findall(OPTION_STRING)
            ]
            new_table.set_course_list(course_list)
            table_list.append(new_table)
        return table_list

    # Check if the output directory for Excel files exists; if not, create it
    if not os.path.isdir(BASE_EXCEL_OUTPUT_PATH):
        os.mkdir(BASE_EXCEL_OUTPUT_PATH)

    # Iterate through XML files in the specified directory
    for file in os.listdir(BASE_XML_INPUT_PATH):
        xml_content = ET.parse(f"{BASE_XML_INPUT_PATH}/{file}")
        root = xml_content.getroot()

        # Extract and format course name
        course_name = root.attrib.get(COURSE_NAME_STRING).replace('  ', ' ').replace('/', '_')
        course_name = course_name[9: course_name.find(')')+1]

        # Create a directory for the course if it doesn't exist
        if not os.path.exists(f"{BASE_EXCEL_OUTPUT_PATH}/{course_name}"):
            os.makedirs(f"{BASE_EXCEL_OUTPUT_PATH}/{course_name}")

        # Dictionary to store correlation data for both semesters
        all_correlation_data = {'Semester1': {}, 'Semester2': {}}
        courses_all_specializations_sem1 = []
        courses_all_specializations_sem2 = []

        # Iterate through each specialization (major track)
        for specialization in root:
            output_path = f"{BASE_EXCEL_OUTPUT_PATH}/{course_name}/"
            specialization_name = specialization.attrib.get(COURSE_NAME_STRING).replace('"', "")

            # Ensure the directory for the specialization exists
            if not os.path.exists(output_path + specialization_name.replace('/', '_')):
                try:
                    os.makedirs(output_path + specialization_name)
                except:
                    print(f"Could not create directory for specialization {specialization_name}", course_name)
                    continue
            output_path = output_path + specialization_name + '/'

            # Lists to store courses and correlation data per semester
            courses_semester_1 = []
            courses_semester_2 = []
            correlation_data = {}

        # Generate and store correlation matrices
        all_specialization_correlation_sem1 = generate_all_correlations('Semester1')
        sorted_courses_sem1 = sorted(list(set(courses_all_specializations_sem1)))
        size = len(sorted_courses_sem1) + 2
        matrix_semester_1 = populate_correlation_matrix(sorted_courses_sem1, size, all_specialization_correlation_sem1)
        save_to_excel(size, matrix_semester_1, f"{course_name.split(' (')[0]}_semester1.xlsx")
