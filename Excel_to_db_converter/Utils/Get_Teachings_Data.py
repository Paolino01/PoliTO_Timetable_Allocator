import glob
import os
import pandas
from openpyxl.styles.builtins import title

from Data.DbApi import DbApi

'''
    Get the list of all Teachings from the Excel file "Percorsi-gruppi-insegnamenti aa 2026.xlsx" and insert them in the DB
'''
def get_teachings():
    db_api = DbApi()
    df = pandas.read_excel('../Data/Excels/Courses Data/Courses List/Percorsi-gruppi-insegnamenti aa 2026.xlsx')
    filtered_df = df.loc[df["ID_COLLEGIO"].isin(["CL003", "CL006"])]

    teachings_to_exclude = ["Prova finale", "Lingua inglese I livello", "Lingua cinese", "Tirocinio", "English Language 1st level", "Final Project", "Thesis", "Internship", "Challenge", "Tesi", "Final project work", "TOP-UIC - Informatica"]

    teaching_name = ""
    id_teaching = 0

    for index, row in filtered_df.iterrows():
        print(row["TITOLO_SS"])
        if row["TITOLO_SS"] != "" and row["TITOLO_SS"] != "nan" and row["TITOLO_SS"] not in teachings_to_exclude:
            id_teaching = row["COD_INS_SS"]
            teaching_name = row["TITOLO_SS"]
        else:
            if row["TITOLO_S"] != "" and row["TITOLO_S"] != "nan" and row["TITOLO_S"] not in teachings_to_exclude:
                id_teaching = row["COD_INS_S"]
                teaching_name = row["TITOLO_S"]
            else:
                if row["TITOLO"] not in teachings_to_exclude:
                    id_teaching = row["COD_INS"]
                    teaching_name = row["TITOLO"]

        # If the Teacher's ID is 11518, then that teacher has not been assigned yet
        if row["MATRICOLA"] == 11518:
            teacher_id = "Docente_" + row["ID_INC"]
        else:
            teacher_id = row["MATRICOLA"]

        if teaching_name != "":
            db_api.insert_teachings(
                row["TIPO_LAUREA"],
                row["NOME_CDL"],
                row["DESC_ORI"],
                row["ID_INC"],
                id_teaching,
                row["ID_COLLEGIO"],
                teaching_name,
                row["CFU"],
                row["MATRICOLA"],
                teacher_id,
                # TODO: we need the information about the Teaching Type
                row["ANNO"] + "-" + row["PERIODO_INI"],
                row["NUMCOR"]
            )

'''
    Calculate the correlation between Teachings according to the Teaching Type
'''
def calculate_correlations():
    db_api = DbApi()

    orientations = db_api.get_orientations()

    for orientation in orientations:
        teachings = db_api.get_teachings_in_orientation(orientation)
        for t1 in teachings:
            for t2 in teachings:
                corr = 0

                # 0: ID_INC, 1: Teaching type, 2: Didactic Period, 3: Alphabetic
                # TODO: we need to check if two Teachings have the same language
                if t1[0] > t2[0] and t1[2] == t2[2] and t1[3] == t2[3]:
                    if t1[1] == "Obbligatorio" or t2[1] == "Obbligatorio":
                        corr = 100
                    else:
                        if t1[1] == "Credito_libero_consigliato" or t2[1] == "Credito_libero_consigliato":
                            corr = 95
                        else:
                            if t1[1] == "Obbligatorio_a_scelta" or t2[1] == "Obbligatorio_a_scelta":
                                corr = 90
                            else:
                                corr = 20

                db_api.insert_correlation(t1[0], t2[0], corr)

'''
    Get the information about the teachers, they hours, and the type of their lectures for each Teaching, using the column "Collaboratori" (Collaborators)
    Collaborators are in the format: (ID) NAME (SOMETHING) [DEPARTMENT] tit: TITLE tipo did:LECTURE_TYPE lin:LANGUAGE - h:  hh.mm;
    PAY ATTENTION TO THE SPACES, SOME FIELDS HAVE SPACES OTHER DON'T. After "h:" there is a double space
    I'm interested only to the teachers who have tit=IN
'''
def get_teaching_teachers(row, main_teacher_id):
    collaborators_string = row['Collaboratori']
    if collaborators_string == "" or collaborators_string == "No coll.":
        return

    db_api = DbApi()

    collaborators = collaborators_string.split(';')
    for c in collaborators:
        coll_info = c.strip().split(' ')

        offset = 0
        if coll_info[2][0] != '(':
            offset = 1
            if coll_info[3][0] != '(':
                offset = 2
                if coll_info[4][0] != '(':
                    offset = 3

        # NOTE: sometimes in the column number 3 there might be the department instead of the keyword "tit:" (titolo).
        # If so, I delete the column number 3
        if coll_info[3 + offset] != 'tit:':
            del(coll_info[3 + offset])

        # The Teacher ID is in the format (ID) in the DB. I convert it to the format 0000ID
        teacher_id = coll_info[0][1:-1].zfill(6)

        # Considering only the Teachers who have title = "IN" and didactic type = "L", "EA" or "EL"
        # Or the Main Teacher independently of the title
        if main_teacher_id == coll_info[0]:
            if coll_info[6 + offset].split(":")[1] == "L":
                db_api.add_teacher_hours(main_teacher_id, coll_info[-1], "L", row["id_inc"])
            else:
                if coll_info[6 + offset].split(":")[1] in ("EA", "EL"):
                    db_api.add_teacher_in_teaching(main_teacher_id, coll_info[-1], coll_info[6 + offset].split(":")[1], row["id_inc"])
        else:
            if coll_info[4 + offset] == "IN" and coll_info[6 + offset].split(":")[1] in ("L", "EA", "EL"):
                db_api.add_teacher_in_teaching(teacher_id, coll_info[-1], coll_info[6 + offset].split(":")[1], row["id_inc"])

def get_teaching_information(teachings):
    db_api = DbApi()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    db_api.delete_teacher_in_teaching()

    for f in courses_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)
        filtered_df = df.loc[df["id_inc"].isin([t.id_teaching for t in teachings])]

        for index, row in filtered_df.iterrows():
            # Adding the information about hours of lectures to a Teaching

            # Getting the Main Teacher ID
            # Need to convert to int first and then to string, since row["matricola"] is considered a float
            main_teacher_id = str(int(row["matricola"])).zfill(6)
            db_api.add_teacher_and_lecture_hours_to_course(row["id_inc"], row["h_lez"], main_teacher_id)

            get_teaching_teachers(row, main_teacher_id)

    print("Lecture and Teachers hours inserted in the DB")