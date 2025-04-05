# from dbAPI import dbAPI
# import os, json
# from constantsScraper import *
# import pandas as pd
# import numpy as np

# def __main__(dbPath, semestre:int):
#     def get_matrix(path_file):
#         xls = pd.read_excel(path_file, header=None)
#         lato = xls.shape[1]
#         size = lato**2
#         return xls.to_numpy(np.array([None]*(size)).reshape(lato,lato).dtype)

#     def gen_single_correlazione(info_correlazioni):
#         for id_inc_1, val in info_correlazioni.items():
#             for id_inc_2, corr_list in val.items():
#                 info_correlazioni[id_inc_1][id_inc_2] = max(corr_list)

#     info_correlazioni = {}
#     db:dbAPI = dbAPI(dbPath)

#     #for dir in os.listdir(BASE_PATH_FILE_EXCEL):
#     path = BASE_PATH_FILE_RESULT_XML
#     for element in os.listdir(path):
#         #path = f"{BASE_PATH_FILE_EXCEL}/{dir}"
#         #if(not os.path.isdir(path)):
#         #    continue
#         #for element in os.listdir(path):
#         path_file = f"{path}/{element}"
#         if(os.path.isdir(path_file) or not element.endswith(f"{semestre}.xlsx")):
#             continue

#         matrix = get_matrix(path_file)
#         lato = len(matrix)


#         for column in range(2,lato):
#             cod_ins_1 = matrix[1,column]
#             ids_inc_1 = db.get_ID_INC_from_codIns(cod_ins_1)
#             if(not ids_inc_1):
#                 continue
#             for row in range(column+1,lato):
#                 cod_ins_2 = matrix[row,1]
#                 corr = matrix[row,column]
#                 ids_inc_2 = db.get_ID_INC_from_codIns(cod_ins_2)
#                 if(not ids_inc_2):
#                     continue
#                 for id1 in ids_inc_1:
#                     for id2 in ids_inc_2:
#                         if id1[0] == id2:
#                             continue
#                         alf1 = db.get_Alfabetiche_ofInsegnamento(id1[0])[0][0]
#                         alf2 = db.get_Alfabetiche_ofInsegnamento(id2[0])[0][0]
#                         if alf1 != '0' and alf2 != '0' and alf1 != alf2:
#                             continue
#                         if(id1[0] in info_correlazioni and id2[0] in info_correlazioni):
#                             if(id2[0] in info_correlazioni[id1[0]]):
#                                 info_correlazioni[id1[0]][id2[0]].append(corr)
#                             elif(id1[0] in info_correlazioni[id2[0]]):
#                                 info_correlazioni[id2[0]][id1[0]].append(corr)
#                             else:
#                                 info_correlazioni[min(id1[0],id2[0])][max(id1[0],id2[0])] = [corr]
#                         elif(id1[0] in info_correlazioni or id2[0] in info_correlazioni):
#                             if id1[0] in info_correlazioni and id2[0] in info_correlazioni[id1[0]]:
#                                 info_correlazioni[id1[0]][id2[0]].append(corr)
#                             elif id2[0] in info_correlazioni and id1[0] in info_correlazioni[id2[0]]:
#                                 info_correlazioni[id2[0]][id1[0]].append(corr)
#                             else:
#                                 try:
#                                     info_correlazioni[id1[0]][id2[0]] = [corr]
#                                 except KeyError:
#                                     info_correlazioni[id2[0]][id1[0]] = [corr]
#                         else:
#                             info_correlazioni[min(id1[0],id2[0])] = {max(id1[0],id2[0]): [corr]}

#     with open("sovrapposizioniManuali.txt", "r") as sovrapFile:
#         for line in sovrapFile:
#             line = line.strip()
#             print(line)
#             titolo = line.split("-")[0]
#             ids = line.split("-")[1]
#             id1 = int(ids.split(";")[0]) 
#             id2 = int(ids.split(";")[1])
#             if id1 not in info_correlazioni:
#                 info_correlazioni[id1] = {id2: [100]}
#             else:
#                 info_correlazioni[id1][id2] = [100]
#             print(f"inseriti constraint {titolo}\n")
                

#     gen_single_correlazione(info_correlazioni)
#     with open('info_corr.json', 'w') as f:
#         f.write(json.dumps(info_correlazioni, indent=4))
#     db.clear_info_correlazioni()
#     for id1, val in info_correlazioni.items():
#         for id2, corr in val.items():
#             if(corr != 0):
#                 db.insert_info_correlazione(min(id1,id2),max(id1,id2),corr)

# #dbPath = "C:/Users/manue/Desktop/allocatore_orario_polito_2223/data/Db_Insegnamenti2024_sol10Luglio_vm2.db"
# #semestre = "semestre1"



from dbAPI import dbAPI
import os, json
from constantsScraper import *
import pandas as pd
import numpy as np

def main(db_path, semester: int):
    """
    Main function to process course correlation data from Excel files,
    convert course codes into unique IDs, and store the results in a database.
    """

    def read_correlation_matrix(file_path):
        """
        Reads an Excel file and returns its content as a NumPy matrix.

        Args:
            file_path (str): Path to the Excel file.

        Returns:
            np.array: Matrix representation of the Excel file.
        """
        excel_data = pd.read_excel(file_path, header=None)
        matrix_size = excel_data.shape[1]
        total_size = matrix_size ** 2
        return excel_data.to_numpy(np.array([None] * (total_size)).reshape(matrix_size, matrix_size).dtype)

    def extract_max_correlation(correlation_data):
        """
        Processes the correlation data dictionary to store only the maximum correlation value 
        for each pair of courses.

        Args:
            correlation_data (dict): Dictionary containing correlation values.
        """
        for course_id_1, values in correlation_data.items():
            for course_id_2, correlation_values in values.items():
                correlation_data[course_id_1][course_id_2] = max(correlation_values)

    # Dictionary to store course correlation information
    correlation_data = {}

    # Initialize database connection
    db: dbAPI = dbAPI(db_path)

    # Path to the directory containing Excel results
    result_directory = BASE_PATH_FILE_RESULT_XML
    for file in os.listdir(result_directory):
        file_path = f"{result_directory}/{file}"

        # Skip directories and files that do not match the specified semester
        if os.path.isdir(file_path) or not file.endswith(f"{semester}.xlsx"):
            continue

        # Load the correlation matrix from the Excel file
        correlation_matrix = read_correlation_matrix(file_path)
        matrix_size = len(correlation_matrix)

        # Iterate over the matrix columns (starting from the 2nd index)
        for column in range(2, matrix_size):
            course_code_1 = correlation_matrix[1, column]
            course_ids_1 = db.get_course_id_from_code(course_code_1)
            if not course_ids_1:
                continue

            # Iterate over matrix rows to compare with the current column
            for row in range(column + 1, matrix_size):
                course_code_2 = correlation_matrix[row, 1]
                correlation_value = correlation_matrix[row, column]
                course_ids_2 = db.get_course_id_from_code(course_code_2)
                if not course_ids_2:
                    continue

                # Compare each pair of course IDs and store correlation values
                for id1 in course_ids_1:
                    for id2 in course_ids_2:
                        if id1[0] == id2:
                            continue
                        
                        # Retrieve alphabetical category codes for validation
                        category_1 = db.get_alphabetical_category(id1[0])[0][0]
                        category_2 = db.get_alphabetical_category(id2[0])[0][0]
                        
                        # Skip correlation if both courses belong to different categories
                        if category_1 != '0' and category_2 != '0' and category_1 != category_2:
                            continue

                        # Store the correlation value in the dictionary
                        if id1[0] in correlation_data and id2[0] in correlation_data:
                            if id2[0] in correlation_data[id1[0]]:
                                correlation_data[id1[0]][id2[0]].append(correlation_value)
                            elif id1[0] in correlation_data[id2[0]]:
                                correlation_data[id2[0]][id1[0]].append(correlation_value)
                            else:
                                correlation_data[min(id1[0], id2[0])][max(id1[0], id2[0])] = [correlation_value]
                        elif id1[0] in correlation_data or id2[0] in correlation_data:
                            if id1[0] in correlation_data and id2[0] in correlation_data[id1[0]]:
                                correlation_data[id1[0]][id2[0]].append(correlation_value)
                            elif id2[0] in correlation_data and id1[0] in correlation_data[id2[0]]:
                                correlation_data[id2[0]][id1[0]].append(correlation_value)
                            else:
                                try:
                                    correlation_data[id1[0]][id2[0]] = [correlation_value]
                                except KeyError:
                                    correlation_data[id2[0]][id1[0]] = [correlation_value]
                        else:
                            correlation_data[min(id1[0], id2[0])] = {max(id1[0], id2[0]): [correlation_value]}

    # Load manually defined course overlaps from a text file
    with open("manual_overlaps.txt", "r") as overlap_file:
        for line in overlap_file:
            line = line.strip()
            print(line)
            title = line.split("-")[0]
            ids = line.split("-")[1]
            id1 = int(ids.split(";")[0])
            id2 = int(ids.split(";")[1])

            # Set manual constraints with a correlation value of 100
            if id1 not in correlation_data:
                correlation_data[id1] = {id2: [100]}
            else:
                correlation_data[id1][id2] = [100]
            print(f"Inserted manual constraint: {title}\n")

    # Process correlation data to retain only the highest values
    extract_max_correlation(correlation_data)

    # Save correlation data to a JSON file
    with open('correlation_data.json', 'w') as file:
        file.write(json.dumps(correlation_data, indent=4))

    # Clear old correlation data from the database
    db.clear_correlation_data()

    # Insert new correlation data into the database
    for id1, values in correlation_data.items():
        for id2, correlation in values.items():
            if correlation != 0:
                db.insert_correlation_data(min(id1, id2), max(id1, id2), correlation)

# Example usage (commented out):
# db_path = "C:/Users/manue/Desktop/schedule_allocator_2023/data/CourseDatabase2024.db"
# semester = "semester1"
