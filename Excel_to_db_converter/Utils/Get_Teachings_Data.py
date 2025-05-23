import glob
import math
import os
import pandas
from openpyxl.styles.builtins import title

from Data.DbApi import DbApi

'''
    Given a row of the Excel file that represents a Teaching, return the type of that Teaching
'''

def get_teaching_type(teaching_row):
    # TODO: I don't have the "Credito_libero_consigliato" category

    teaching_type = ""

    if (
            "Insegnamento a scelta" not in teaching_row["TITOLO"] and
            "Crediti liberi" not in teaching_row["TITOLO"] and
            "Choice from table" not in teaching_row["TITOLO"] and
            "Free ECTS credits" not in teaching_row["TITOLO"] and
            "Free choice" not in teaching_row["TITOLO"] and
            "Introductive Seminars" not in teaching_row["TITOLO"] and
            "Elective course" not in teaching_row["TITOLO"]
    ):
        teaching_type = "Obbligatorio"
    else:
        if (
                str(teaching_row["TITOLO_S"]) != "nan" and
                "Crediti liberi" not in teaching_row["TITOLO_S"] and
                "Choice from table" not in teaching_row["TITOLO_S"] and
                "Free ECTS credits" not in teaching_row["TITOLO_S"] and
                "Free choice" not in teaching_row["TITOLO_S"]
        ):
            teaching_type = "Obbligatorio_a_scelta"
        else:
            teaching_type = "Tabella_a_scelta"

    return teaching_type

'''
    Get the list of all Teachings from the Excel file "Percorsi-gruppi-insegnamenti aa 2026.xlsx" and insert them in the DB
'''
def get_teachings():
    db_api = DbApi()
    teachings_to_exclude = ["Prova finale", "Lingua inglese I livello", "Lingua cinese", "Tirocinio",
                            "English Language 1st level", "Final Project", "Thesis", "Internship", "Challenge", "Tesi",
                            "Final project work", "TOP-UIC - Informatica"]

    df = pandas.read_excel('../Data/Excels/Courses Data/Courses List/Percorsi-gruppi-insegnamenti aa 2026.xlsx', dtype=str, na_values="")
    filtered_df = df[
        (df["ID_COLLEGIO"].isin(["CL003", "CL006"])) &
        (df["PERIODO_INI"] == "1") &
        ((df["TIPO_LAUREA"] == "Z") | ((df["TIPO_LAUREA"] == "1") & (df["ANNO"] != "1"))) &
        (~df["TITOLO"].isin(teachings_to_exclude)) &
        (~df["TITOLO_S"].isin(teachings_to_exclude)) &
        (~df["TITOLO_SS"].isin(teachings_to_exclude)) &
        (~df["TITOLO"].str.contains("Challenge", regex=False, na=False)) &
        (~df["TITOLO_S"].str.contains("Challenge", regex=False, na=False)) &
        (~df["TITOLO_SS"].str.contains("Challenge", regex=False, na=False))
    ]

    db_api.delete_all_teachings()

    for index, row in filtered_df.iterrows():
        if str(row["ID_INC"]) != "nan":
            # Get the name and ID of a Teaching
            teaching_name = ""
            id_teaching = 0
            if row["TITOLO_SS"] != "" and str(row["TITOLO_SS"]) != "nan":
                    id_teaching = row["COD_INS_SS"]
                    teaching_name = row["TITOLO_SS"]
            else:
                if row["TITOLO_S"] != "" and str(row["TITOLO_S"]) != "nan":
                        id_teaching = row["COD_INS_S"]
                        teaching_name = row["TITOLO_S"]
                else:
                    id_teaching = row["COD_INS"]
                    teaching_name = row["TITOLO"]

            # If the Teacher's ID is 11518, then that teacher has not been assigned yet
            if teaching_name != "":
                if row["MATRICOLA"] == "11518" or str(row["MATRICOLA"]) == 'nan':
                    teacher_id = "Docente_" + row["ID_INC"]
                else:
                    teacher_id = row["MATRICOLA"].zfill(6)

                # Get the Type of Teaching
                teaching_type = get_teaching_type(row)

                db_api.insert_teachings(
                    row["TIPO_LAUREA"],
                    row["NOME_CDL"],
                    row["DESC_ORI"],
                    row["ID_INC"],
                    id_teaching,
                    row["ID_COLLEGIO"],
                    teaching_name,
                    row["CFU"],
                    teacher_id,
                    teaching_type,
                    row["ANNO"] + "-" + row["PERIODO_INI"],
                    row["NUMCOR"]
                )

    print("Teachings inserted in the DB")

'''
    Calculate the correlation between Teachings according to the Teaching Type
'''
def calculate_correlations():
    db_api = DbApi()
    teachings_to_exclude = ["Prova finale", "Lingua inglese I livello", "Lingua cinese", "Tirocinio",
                            "English Language 1st level", "Final Project", "Thesis", "Internship", "Challenge", "Tesi",
                            "Final project work", "TOP-UIC - Informatica"]

    db_api.remove_correlation_info()

    orientations = db_api.get_orientations()
    df = pandas.read_excel('../Data/Excels/Courses Data/Courses List/Percorsi-gruppi-insegnamenti aa 2026.xlsx', dtype=str, na_values="")

    for orientation in orientations:
        filtered_df = df[
            (df["DESC_ORI"] == orientation[0]) &
            (df["NOME_CDL"] == orientation[1]) &
            (df["TIPO_LAUREA"] == orientation[2]) &
            (df["PERIODO_INI"] == "1") &
            ((df["TIPO_LAUREA"] == "Z") | ((df["TIPO_LAUREA"] == "1") & (df["ANNO"] != "1"))) &
            (~df["TITOLO"].isin(teachings_to_exclude)) &
            (~df["TITOLO_S"].isin(teachings_to_exclude)) &
            (~df["TITOLO_SS"].isin(teachings_to_exclude)) &
            (~df["TITOLO"].str.contains("Challenge", regex=False, na=False)) &
            (~df["TITOLO_S"].str.contains("Challenge", regex=False, na=False)) &
            (~df["TITOLO_SS"].str.contains("Challenge", regex=False, na=False))
        ]

        for index1, t1 in filtered_df.iterrows():
            for index2, t2 in filtered_df.iterrows():
                # This variable is needed to know if at least one of the two correlated Teachings is mandatory
                mandatory = 0

                if (
                    str(t1["ID_INC"]) != "nan" and str(t2["ID_INC"]) != "nan" and
                    t1["ID_INC"] > t2["ID_INC"] and
                    t1["PERIODO_INI"] == t2["PERIODO_INI"] and
                    t1["ANNO"] == t2["ANNO"] and
                    (t1["NUMCOR"] == t2["NUMCOR"] or t1["NUMCOR"] == "0" or t2["NUMCOR"] == "0") and
                    t1["TITOLO"] != t2["TITOLO"]
                ):
                    t1_type = get_teaching_type(t1)
                    t2_type = get_teaching_type(t2)

                    if t1_type == "Tabella_a_scelta" or t2_type == "Tabella_a_scelta":
                        # At least on of the two Teachings is "Tabella_a_scelta"
                        corr = 20
                        if t1_type == "Obbligatorio" or t2_type == "Obbligatorio":
                            mandatory = 1
                    else:
                        if t1_type == "Obbligatorio" and t2_type == "Obbligatorio":
                            # Both Teachings are "Obbligatori"
                            corr = 100
                            mandatory = 1
                        else:
                            # One "Obbligatorio" and one "Obbligatorio_a_scelta" or both "Obbligatorio_a_scelta"
                            if t1_type == "Obbligatorio_a_scelta":
                                corr = math.floor(100/(filtered_df["TITOLO"] == t1["TITOLO"]).sum())
                            else:
                                corr = math.floor(100/(filtered_df["TITOLO"] == t2["TITOLO"]).sum())

                            if t1_type == "Obbligatorio" or t2_type == "Obbligatorio":
                                mandatory = 1

                    db_api.insert_correlation(t1["ID_INC"], t2["ID_INC"], corr, mandatory)

    print("Correlations inserted in the DB")

'''
    Get the information about the teachers, their hours, and the type of their lectures for each Teaching, using the column "Collaboratori" (Collaborators)
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