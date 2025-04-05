# import networkx as nx
# import xml.etree.ElementTree as et
# import pandas as pd
# import os, json
# from itertools import combinations
# from constantsScraper import *
# from Script_calcolo_numero_iscritti.Costanti import *

# """
# Aggiornamento 23/10/2023
# Sto inserendo nel seguente dizionario tutti i parametri che andrebbero configurati prima dell'esecuzione
# """

# parameters = {
#     #Nel file degli studenti iscritti ai vari insegnamenti ho tenuto conto, per le interesenzioni, solo gli studenti 
#     #frequentanti nell'ultimo anno accademico (Nel mio caso 22/23)
#     "ultimoAnnoAccademico": "23",
#     "semestre": "1",
#     "other_semestre": "2",
#     "outputJson": "./Data/Paths/ResultPath.json",
#     "limiteMinimoStudentiPath": 0,
#     "offsetSottoinsiemePath": 40
# }

# def load_matricole(path):
#     mapIdIncToSetMatricole = {}
#     with open("load_matricole_log.txt", "w") as log:
#         for file in os.listdir(path):
#             if not file.endswith('.xls') and not file.split('.')[0].isnumeric():
#                 continue
#             id_inc = file.split('.')[0]
#             set_matricole = set()
#             xls = pd.read_excel(path + '/' + file)
#             res = pd.DataFrame(filter(lambda val: str(val[-1]).endswith(parameters["ultimoAnnoAccademico"]) or str(val[-1]).startswith("Da frequentare"), xls.to_numpy()))
#             if len(res) == 0:
#                 log.write(f'IL FILE {file} non ha prodotto risultati\n')
#                 continue
#             res.columns = xls.columns

#             set_matricole = set(res['MATRICOLA'].unique())
#             if id_inc not in mapIdIncToSetMatricole:
#                 mapIdIncToSetMatricole[id_inc] = set_matricole
#             else:
#                 log(f'ERRORE ID_INC DUPLICATO FILE {file}\n')
#     return mapIdIncToSetMatricole

# def evaluatePaths(cdl, orientamento, anno, paths:list[list]):
#     if cdl not in mapPathToIntersectionValue:
#         mapPathToIntersectionValue[cdl] = {}
#     if orientamento not in mapPathToIntersectionValue[cdl]:
#         mapPathToIntersectionValue[cdl][orientamento] = {}
#     if anno not in mapPathToIntersectionValue[cdl][orientamento]:
#         mapPathToIntersectionValue[cdl][orientamento][anno] = {}

#     new_paths = [sorted([p.split("_")[-1] for p in path[1:-1]]) for path in paths]
#     str_path_dict = {}
#     for real_path in new_paths:
#         is_dummy = 0
#         if "dummy" in real_path:
#             is_dummy = 1
#             real_path.remove("dummy")
#         if len(real_path) == 2:
#             continue

#         str_path = "_".join(real_path)

#         data_missing_nodes = []
#         data_nodes = []
#         for node in real_path:
#             if node not in mapIdIncToSetMatricole.keys():
#                 data_missing_nodes.append(node)
#             else:
#                 data_nodes.append(node)
        
#         if not data_nodes:
#             mapPathToIntersectionValue[cdl][orientamento][anno][str_path] = -1
#             mapPath[str_path] = -1
#             continue
        
#         for i in range(len(data_nodes),len(data_nodes)-1, -1):
#             combList = list(combinations(data_nodes, i))
#             for com in combList:
#                 nodes = list(com)
#                 res:set = set(mapIdIncToSetMatricole[nodes[0]])
#                 for node in nodes[1:]:
#                     res.intersection_update(mapIdIncToSetMatricole[node])
#                 if len(res)>=parameters["limiteMinimoStudentiPath"] and len(data_nodes) > 1:
#                     pathInseriti = list(mapPath.keys())
#                     #Il filtro prende tutti i percorsi di cui il percorso che si sta studiando è sottoinsieme
#                     pathInseritiFiltered = list(filter(lambda path: all(node in path for node in nodes) and len(nodes) < len(path.split("_")), pathInseriti))
#                     """
#                     Se il sottinsieme ha un numero di studenti non troppo maggiore rispetto al suo sovrainsieme
#                     preferirò per efficenza non considerare il sottoinseme nei path finale, dato che
#                     il sovrainsieme sarà sufficiente per creare i vincoli anche a lui appartenenti
#                     """
#                     if any(len(res) in range(mapPath[path], mapPath[path]+parameters["offsetSottoinsiemePath"]) for path in pathInseritiFiltered):
#                         print(f"i am skipping {'_'.join(nodes)} because of {pathInseritiFiltered}")
#                         if "_".join(nodes) in mapPath:
#                             del mapPath["_".join(nodes)]
#                         continue
#                     """if data_missing_nodes:
#                         log.write(f"In path: {real_path} nodes: {data_missing_nodes} are missing from data\n")
#                         if "_".join(nodes) in str_path_dict:
#                             str_path_dict["_".join(nodes)].update({"_".join(nodes): len(res)})
#                         else:
#                             str_path_dict["_".join(nodes)] = {"_".join(nodes): len(res)}
#                     else: """
#                     mapPathToIntersectionValue[cdl][orientamento][anno]["_".join(nodes)] = len(res)
#                     mapPath["_".join(nodes)] = len(res)
                    
#             """                     
#         res:set = set(mapIdIncToSetMatricole[data_nodes[0]])
#         for node in data_nodes[1:]:
#             res.intersection_update(mapIdIncToSetMatricole[node])
#         if res:
#             if data_missing_nodes and len(data_nodes) > 1:
#                 log.write(f"In path: {real_path} nodes: {data_missing_nodes} are missing from data\n")
#                 if "_".join(data_nodes) in str_path_dict:
#                     str_path_dict["_".join(data_nodes)].update({"_".join(data_nodes): len(res)})
#                 else:
#                     str_path_dict["_".join(data_nodes)] = {"_".join(data_nodes): len(res)}
#             else:
#                 mapPathToIntersectionValue[cdl][orientamento][anno][str_path] = len(res)
#                 if (len(str_path.split("_")) > 1):
#                     mapPath[str_path] = len(res) """


#     """ for group, dict in str_path_dict.items():
#         for str_path in str_path_dict[group]:
#             division_factor = len(list(filter(lambda path: len(path) == len(str_path), str_path_dict[group])))
#             str_path_dict[group][str_path] //= division_factor
#             if str_path in mapPath:
#                 mapPath[str_path] = max(mapPath[str_path], str_path_dict[group][str_path])
#             else:
#                 mapPath[str_path] = str_path_dict[group][str_path]
#         mapPathToIntersectionValue[cdl][orientamento][anno].update(str_path_dict[group]) """


# def get_tabelle_semestre(periodi):
#     tabelle_semestre = []
#     for periodo in periodi:
#         if periodo.find(SEMESTRE_STRING).text != parameters["semestre"]:
#             continue
#         ins_list = periodo.find(NOME_LISTA_INSEGNAMENTI_XML)
#         tabelle_semestre.extend(
#             ins.get(NOME_TABELLA_STRING)
#             for ins in ins_list
#             if NOME_TABELLA_STRING in ins.attrib.keys() and len(ins) > 0
#         )
#     return tabelle_semestre     

# def insert_into_graph(id_inc_list, cod_ins, nome_tab= "", is_tab_in_both_semesters=False):
#     nodes = []
#     if id_inc_list:
#         for node in prevNodes:
#             if is_tab_in_both_semesters:
#                 G.add_edge(node, "dummy")
#             for id_inc in id_inc_list:
#                 new_node = nome_tab + "_" + str(id_inc) if nome_tab else str(id_inc)
#                 G.add_edge(node, new_node)
#                 nodes.append(new_node)
#     else:
#         log.write("COD_INS: "+cod_ins+" non ha dato risultato all'interno del file excel\n")
#         for node in prevNodes:
#             if is_tab_in_both_semesters:
#                 G.add_edge(node, "dummy")
#             new_node = nome_tab + "_" + cod_ins if nome_tab else cod_ins
#             G.add_edge(node, new_node)
#         nodes.append(new_node)
#     return nodes

# semestre = parameters[SEMESTRE_STRING]
# other_semestre = parameters["other_semestre"]

# G = nx.DiGraph()
# G.add_node("Start")

# xls_gof = pd.read_excel(FILE_GOF)
# mapIdIncToSetMatricole = load_matricole(OUTPUT_PATH_ID_INC)
# mapPathToIntersectionValue = {}
# mapPathToIntersectionValueNoCodIns = {}
# mapPath = {}

# df:pd.DataFrame = xls_gof.get(["ID_INC", "COD_INS"])
# with open("grafi_log.txt", "w",encoding="utf-8") as log:
#     log.write("THIS LOG IS GENERATED BY [gen_path_studenti.py]\n\n")
#     for file in os.listdir(BASE_PATH_FILE_XML):
#         root = et.parse(BASE_PATH_FILE_XML + '/' + file).getroot()
#         orientamenti = root.findall('orientamento')

#         for orientamento in orientamenti:
#             periodi = orientamento.findall(PERIODO_STRING)
#             tabelle_semestre = get_tabelle_semestre(periodi)

#             for periodo in periodi:
#                 if periodo.find(SEMESTRE_STRING).text == other_semestre or (periodo.find(ANNO_STRING).text == semestre and "Magistrale" not in file):
#                     continue
#                 insegnamenti = periodo.find(NOME_LISTA_INSEGNAMENTI_XML)
#                 G = nx.DiGraph()
#                 G.add_node("Start")
#                 prevNodes = ["Start"]

#                 for ins in insegnamenti:
#                     #Singolo insegnamento obbliatorio
#                     if NOME_STRING in ins.attrib.keys():
#                         cod_ins = ins.text
#                         currNodes = insert_into_graph(
#                             set(df[df["COD_INS"] == cod_ins]
#                             .get("ID_INC")
#                             .to_numpy()), cod_ins)
#                     else:
#                         if ins.tag == NOME_SCELTA_TABELLA_LINGUA_XML:
#                             tabelle_lingua = ins.findall(NOME_TABELLA_LINGUA_XML)
#                             ins_tab_1 = tabelle_lingua[0].findall(INSEGNAMENTO_STRING)
#                             ins_tab_2 = tabelle_lingua[1].findall(INSEGNAMENTO_STRING)
#                             if len(ins_tab_1) != len(ins_tab_2):
#                                 log.write("ERRORE: Scelta_tabella_lingua con dimensioni differenti "+ orientamento.get(NOME_STRING) + "  " + file)
#                             for i in range(len(ins_tab_1)):
#                                 currNodes.extend(insert_into_graph(
#                                     set(df[df["COD_INS"] == ins_tab_1[i].text]
#                                     .get("ID_INC")
#                                     .to_numpy()), ins_tab_1[i].text))
#                                 currNodes.extend(insert_into_graph(
#                                     set(df[df["COD_INS"] == ins_tab_2[i].text]
#                                     .get("ID_INC")
#                                     .to_numpy()), ins_tab_2[i].text))
#                             continue
#                         if ins.find(OPZIONE_STRING) is None:
#                             continue
#                         currNodes = []
#                         if NOME_TABELLA_STRING not in ins.attrib.keys():
#                             for opt in ins:
#                                 cod_ins = opt.text
#                                 currNodes.extend(insert_into_graph(
#                                     set(df[df["COD_INS"] == cod_ins]
#                                     .get("ID_INC")
#                                     .to_numpy()), cod_ins))
#                         else:
#                             nome_tab = ins.get(NOME_TABELLA_STRING)
#                             if nome_tab in tabelle_semestre:
#                                 currNodes.append("dummy")
#                             for opt in ins:
#                                 if cod_ins := opt.text:
#                                     currNodes.extend(insert_into_graph(
#                                         set(df[df["COD_INS"] == cod_ins]
#                                         .get("ID_INC")
#                                         .to_numpy()), cod_ins, nome_tab, nome_tab in tabelle_semestre))
#                     prevNodes = currNodes
#                 for node in prevNodes:
#                     G.add_edge(node, "End")
#                 try:
#                     paths = nx.all_shortest_paths(G, "Start", "End")
#                     paths = list(filter(lambda path: len(path) == len({p.split("_")[-1] for p in path}), paths))
#                     for path in paths:
#                         print(path, "| Orientamento: " + orientamento.get(NOME_STRING), "| Anno: " + periodo.find(ANNO_STRING).text)
#                     evaluatePaths(root.get(NOME_STRING), orientamento.get(NOME_STRING), periodo.find(ANNO_STRING).text, paths)
#                 except Exception as e:
#                     print(e, root.get(NOME_STRING), orientamento.get(NOME_STRING), periodo.find(SEMESTRE_STRING).text, periodo.find(ANNO_STRING).text)
#                     #print(G.edges)
#                     exit()

#             print("Done")

# #mapPathToIntersectionValue = dict(sorted(mapPathToIntersectionValue.items(), key=lambda item: item[1], reverse=True))
# for cdl in mapPathToIntersectionValue:
#     for orientamento in mapPathToIntersectionValue[cdl]:
#         for anno in mapPathToIntersectionValue[cdl][orientamento]:
#             if cdl not in mapPathToIntersectionValueNoCodIns:
#                 mapPathToIntersectionValueNoCodIns[cdl] = {}
#             if orientamento not in mapPathToIntersectionValueNoCodIns[cdl]:
#                 mapPathToIntersectionValueNoCodIns[cdl][orientamento] = {}
#             mapPathToIntersectionValueNoCodIns[cdl][orientamento][anno] = dict(filter(lambda pair: all(id_inc.isnumeric() for id_inc in pair[0].split('_')), mapPathToIntersectionValue[cdl][orientamento][anno].items())) 


# """ with open("result.json", "w") as res:
#     json.dump(mapPathToIntersectionValue, res, indent=4)
# with open("resultNoCodIns.json", "w") as resNoCodIns:
#     json.dump(mapPathToIntersectionValueNoCodIns, resNoCodIns, indent=4) """

# mapToWrite = dict(filter(lambda pair: all(id_inc.isnumeric() for id_inc in pair[0].split('_')), mapPath.items()))
# mapToWrite = dict(sorted(mapToWrite.items(), key=lambda item: item[1], reverse=True))

# with open(parameters["outputJson"], "w", encoding="utf-8") as resOnlyPath:
#     json.dump(mapToWrite, resOnlyPath, indent=4)


from asyncio import log
import networkx as nx
import xml.etree.ElementTree as et
import pandas as pd
import os, json
from itertools import combinations
from constantsScraper import *
from student_enrollment_processing.Constants import *

"""
Update 10/23/2023
This dictionary contains all parameters that should be configured before execution.
"""

config_params = {
    # In the student enrollment data file, only students attending in the most recent academic year 
    # (in this case, 2022/23) are considered.
    "latest_academic_year": "23",
    "current_semester": "1",
    "other_semester": "2",
    "output_json_path": "./Data/Paths/ResultPath.json",
    "min_students_per_path": 0,
    "subset_offset_limit": 40
}

def load_student_enrollments(directory):
    """
    Loads student enrollment data from Excel files.

    Args:
        directory (str): The directory containing the Excel files.

    Returns:
        dict: A mapping of course IDs to sets of enrolled student IDs.
    """
    course_enrollment_map = {}
    with open("load_student_enrollments_log.txt", "w") as log_file:
        for file in os.listdir(directory):
            if not file.endswith('.xls') and not file.split('.')[0].isnumeric():
                continue
            course_id = file.split('.')[0]
            student_set = set()
            xls_data = pd.read_excel(directory + '/' + file)
            
            # Filter students from the latest academic year or those yet to enroll
            filtered_data = pd.DataFrame(
                filter(
                    lambda val: str(val[-1]).endswith(config_params["latest_academic_year"]) or 
                                str(val[-1]).startswith("To attend"), 
                    xls_data.to_numpy()
                )
            )
            if len(filtered_data) == 0:
                log_file.write(f'The file {file} produced no results\n')
                continue
            filtered_data.columns = xls_data.columns

            student_set = set(filtered_data['STUDENT_ID'].unique())
            if course_id not in course_enrollment_map:
                course_enrollment_map[course_id] = student_set
            else:
                log_file.write(f'ERROR: DUPLICATE COURSE_ID in file {file}\n')
    return course_enrollment_map

def analyze_paths(degree_program, specialization, academic_year, paths:list[list]):
    """
    Analyzes and processes enrollment paths.

    Args:
        degree_program (str): The name of the degree program.
        specialization (str): The name of the specialization.
        academic_year (str): The academic year.
        paths (list[list]): A list of paths (sequences of course enrollments).
    """
    if degree_program not in path_intersection_data:
        path_intersection_data[degree_program] = {}
    if specialization not in path_intersection_data[degree_program]:
        path_intersection_data[degree_program][specialization] = {}
    if academic_year not in path_intersection_data[degree_program][specialization]:
        path_intersection_data[degree_program][specialization][academic_year] = {}

    # Remove redundant labels in paths
    cleaned_paths = [sorted([p.split("_")[-1] for p in path[1:-1]]) for path in paths]
    
    for actual_path in cleaned_paths:
        is_placeholder = 0
        if "dummy" in actual_path:
            is_placeholder = 1
            actual_path.remove("dummy")
        if len(actual_path) == 2:
            continue

        path_str = "_".join(actual_path)
        missing_nodes = []
        valid_nodes = []

        for node in actual_path:
            if node not in course_enrollment_map.keys():
                missing_nodes.append(node)
            else:
                valid_nodes.append(node)
        
        if not valid_nodes:
            path_intersection_data[degree_program][specialization][academic_year][path_str] = -1
            processed_paths[path_str] = -1
            continue

        for i in range(len(valid_nodes), len(valid_nodes) - 1, -1):
            combinations_list = list(combinations(valid_nodes, i))
            for combination in combinations_list:
                nodes = list(combination)
                student_intersection:set = set(course_enrollment_map[nodes[0]])
                for node in nodes[1:]:
                    student_intersection.intersection_update(course_enrollment_map[node])

                if len(student_intersection) >= config_params["min_students_per_path"] and len(valid_nodes) > 1:
                    existing_paths = list(processed_paths.keys())

                    # Filter paths that are supersets of the current path
                    filtered_superset_paths = list(
                        filter(
                            lambda path: all(node in path for node in nodes) and len(nodes) < len(path.split("_")),
                            existing_paths
                        )
                    )
                    
                    # Skip subsets if their student count is close to the superset
                    if any(len(student_intersection) in range(
                        processed_paths[path], 
                        processed_paths[path] + config_params["subset_offset_limit"]
                    ) for path in filtered_superset_paths):
                        print(f"Skipping {'_'.join(nodes)} due to {filtered_superset_paths}")
                        if "_".join(nodes) in processed_paths:
                            del processed_paths["_".join(nodes)]
                        continue

                    path_intersection_data[degree_program][specialization][academic_year]["_".join(nodes)] = len(student_intersection)
                    processed_paths["_".join(nodes)] = len(student_intersection)

def extract_semester_tables(periods):
    """
    Retrieves semester tables from XML data.

    Args:
        periods (list): List of XML period elements.

    Returns:
        list: List of table names for the given semester.
    """
    semester_tables = []
    for period in periods:
        if period.find(SEMESTER_STRING).text != config_params["current_semester"]:
            continue
        course_list = period.find(COURSE_LIST_XML)
        semester_tables.extend(
            course.get(TABLE_NAME_STRING)
            for course in course_list
            if TABLE_NAME_STRING in course.attrib.keys() and len(course) > 0
        )
    return semester_tables     

def add_to_graph(course_id_list, course_code, table_name= "", is_course_in_both_semesters=False):
    """
    Adds nodes to the graph for each course.

    Args:
        course_id_list (list): List of course IDs.
        course_code (str): Course code.
        table_name (str, optional): Table name.
        is_course_in_both_semesters (bool, optional): Indicates if the course is in both semesters.

    Returns:
        list: List of inserted nodes.
    """
    nodes = []
    if course_id_list:
        for prev_node in previous_nodes: # type: ignore
            if is_course_in_both_semesters:
                G.add_edge(prev_node, "dummy")
            for course_id in course_id_list:
                new_node = table_name + "_" + str(course_id) if table_name else str(course_id)
                G.add_edge(prev_node, new_node)
                nodes.append(new_node)
    else:
        log.write("COURSE_CODE: "+course_code+" not found in the Excel file\n")
        for prev_node in previous_nodes: # type: ignore
            if is_course_in_both_semesters:
                G.add_edge(prev_node, "dummy")
            new_node = table_name + "_" + course_code if table_name else course_code
            G.add_edge(prev_node, new_node)
        nodes.append(new_node)
    return nodes

# Initialize parameters
current_semester = config_params["current_semester"]
other_semester = config_params["other_semester"]

# Initialize graph
G = nx.DiGraph()
G.add_node("Start")

# Load student enrollments
xls_data = pd.read_excel(FILE_GOF)
course_enrollment_map = load_student_enrollments(STUDENT_ENROLLMENT_OUTPUT_PATH)
path_intersection_data = {}
path_intersection_no_code = {}
processed_paths = {}

df:pd.DataFrame = xls_data.get(["COURSE_ID", "COURSE_CODE"])

# Save the processed paths in a JSON file
filtered_paths = dict(filter(lambda pair: all(course_id.isnumeric() for course_id in pair[0].split('_')), processed_paths.items()))
sorted_paths = dict(sorted(filtered_paths.items(), key=lambda item: item[1], reverse=True))

with open(config_params["output_json_path"], "w", encoding="utf-8") as output_file:
    json.dump(sorted_paths, output_file, indent=4)
