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
    df = pandas.read_excel('../Data/Excels/Courses Data/Courses List/Percorsi-gruppi-insegnamenti aa 2026.xlsx', dtype=str, na_values="")
    filtered_df = df.loc[df["ID_COLLEGIO"].isin(["CL003", "CL006"])]

    db_api.delete_all_teachings()

    teachings_to_exclude = ["Prova finale", "Lingua inglese I livello", "Lingua cinese", "Tirocinio", "English Language 1st level", "Final Project", "Thesis", "Internship", "Challenge", "Tesi", "Final project work", "TOP-UIC - Informatica"]

    for index, row in filtered_df.iterrows():
        # Get the name and ID of a Teaching
        teaching_name = ""
        id_teaching = 0
        if row["TITOLO_SS"] != "" and str(row["TITOLO_SS"]) != "nan":
            if row["TITOLO_SS"] in teachings_to_exclude or "Challenge" in row["TITOLO_SS"]:
                teaching_name = ""
                id_teaching = 0
            else:
                id_teaching = row["COD_INS_SS"]
                teaching_name = row["TITOLO_SS"]
        else:
            if row["TITOLO_S"] != "" and str(row["TITOLO_S"]) != "nan":
                if row["TITOLO_S"] in teachings_to_exclude or "Challenge" in row["TITOLO_S"]:
                    teaching_name = ""
                    id_teaching = 0
                else:
                    id_teaching = row["COD_INS_S"]
                    teaching_name = row["TITOLO_S"]
            else:
                if row["TITOLO"] not in teachings_to_exclude and "Challenge" not in row["TITOLO"]:
                    id_teaching = row["COD_INS"]
                    teaching_name = row["TITOLO"]

        # If the Teacher's ID is 11518, then that teacher has not been assigned yet
        if row["MATRICOLA"] == 11518:
            teacher_id = "Docente_" + row["ID_INC"]
        else:
            teacher_id = row["MATRICOLA"]

        # Get the Type of Teaching
        # TODO: I don't have the "Credito_libero_consigliato" category
        if (
            "Insegnamento a scelta" not in row["TITOLO"] and
            "Crediti liberi" not in row["TITOLO"] and
            "Choice from table" not in row["TITOLO"] and
            "Free ECTS credits" not in row["TITOLO"]  and
            "Free choice" not in row["TITOLO"] and
            "Introductive Seminars" not in row["TITOLO"] and
            "Elective course" not in row["TITOLO"]
        ):
            teaching_type = "Obbligatorio"
        else:
            if (
                str(row["TITOLO_S"]) != "nan" and
                "Crediti liberi" not in row["TITOLO_S"] and
                "Choice from table" not in row["TITOLO_S"] and
                "Free ECTS credits" not in row["TITOLO_S"] and
                "Free choice" not in row["TITOLO_S"]
            ):
                teaching_type = "Obbligatorio_a_scelta"
            else:
                teaching_type = "Tabella_a_scelta"

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

    db_api.remove_correlation_info()

    orientations = db_api.get_orientations()
    df = pandas.read_excel('../Data/Excels/Courses Data/Courses List/Percorsi-gruppi-insegnamenti aa 2026.xlsx', dtype=str, na_values="")

    for orientation in orientations:
        filtered_df = df[(df["DESC_ORI"] == orientation[0]) & (df["TIPO_LAUREA"] == orientation[1]) & (df["NOME_CDL"] == orientation[2])]
        for index1, t1 in filtered_df.iterrows():
            for index2, t2 in filtered_df.iterrows():
                if (
                    str(t1["ID_INC"]) != "nan" and str(t2["ID_INC"]) != "nan" and
                    t1["ID_INC"] > t2["ID_INC"] and
                    t1["PERIODO_INI"] == t2["PERIODO_INI"] and
                    t1["ANNO"] == t2["ANNO"] and
                    (t1["NUMCOR"] == t2["NUMCOR"] or t1["NUMCOR"] == "0" or t2["NUMCOR"] == "0") and
                    t1["TITOLO"] != t2["TITOLO"]
                ):
                    if (
                        (
                        "Insegnamento a scelta" not in t1["TITOLO"] and
                        "Crediti liberi" not in t1["TITOLO"] and
                        "Choice from table" not in t1["TITOLO"] and
                        "Free ECTS credits" not in t1["TITOLO"] and
                        "Free choice" not in t1["TITOLO"] and
                        "Introductive Seminars" not in t1["TITOLO"] and
                        "Elective course" not in t1["TITOLO"]
                        )
                        or
                        (
                        "Insegnamento a scelta" not in t2["TITOLO"] and
                        "Crediti liberi" not in t2["TITOLO"] and
                        "Choice from table" not in t2["TITOLO"] and
                        "Free ECTS credits" not in t2["TITOLO"] and
                        "Free choice" not in t2["TITOLO"] and
                        "Introductive Seminars" not in t2["TITOLO"] and
                        "Elective course" not in t2["TITOLO"]
                        )
                    ):
                        # At least one of the two Teachings is "Obbligatorio"
                        corr = 100
                    else:
                        if (
                            str(t1["TITOLO_S"]) != "nan" and
                            "Crediti liberi" not in t1["TITOLO_S"] and
                            "Choice from table" not in t1["TITOLO_S"] and
                            "Free ECTS credits" not in t1["TITOLO_S"] and
                            "Free choice" not in t1["TITOLO_S"] and
                            str(t2["TITOLO_S"]) != "nan" and
                            "Crediti liberi" not in t2["TITOLO_S"] and
                            "Choice from table" not in t2["TITOLO_S"] and
                            "Free ECTS credits" not in t2["TITOLO_S"] and
                            "Free choice" not in t2["TITOLO_S"]
                        ):
                            # Both Teachings are "Obbligatori_a_scelta"
                            corr = 90
                        else:
                            # At least on of the two Teachings is "Tabella_a_scelta", and the other is either "Tabella_a_scelta" or "Obbligatorio_a_scelta"
                            # TODO: ask if this is good of if Obbligatorio_a_scelta and Tabella_a_scelta should have a correlation of 90
                            corr = 20

                    db_api.insert_correlation(t1["ID_INC"], t2["ID_INC"], corr)

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