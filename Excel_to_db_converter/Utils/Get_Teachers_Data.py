import glob
import math
import os
import pandas

from Data.DbApi import DbApi

# Dictionaries that match the preferences written in the Excel files with the number of double and single Slots.
# Data is in the format: "preference": [n° double Slots, n° single slots]
lecture_slot_preferences_dict = {
    "tutti i blocchi da 3h": [1, 0],
    "un blocco da 3h e gli altri da 1,5h": [1, 1],
    "tutti i blocchi da 1,5h": [0, 1],
    "un blocco da 4,5h (Atelier per Architettura)": [2, 0],
    "nan": [0, 0]
}

practice_slot_preferences_dict = {
    "tutti i blocchi da 3h per ciascuna squadra": [1, 0],
    "un blocco da 3h e gli altri da 1,5h per ciascuna squadra": [1, 1],
    "tutti i blocchi da 1,5h per ciascuna squadra": [0, 1],
    "un blocco da 4,5h (Atelier per Architettura) per ciascuna squadra": [2, 0],
    "Non applicabile": [0, 0],
    "nan": [0, 0]
}

lab_slot_preferences_dict = {
    "blocchi da 3h per ciascuna squadra": 1,
    "blocchi da 3 h per ciascuna squadra": 1,
    "blocchi da 1.5 h per ciascuna squadra": 0,
    "blocchi da 1,5h per ciascuna squadra": 0,
    "indifferente": 0,
    "nan": 0
}

'''
    Get Practice organization preferences from the Excel file
'''
def get_practice_preferences(row):
    practice_hours = int(row["NUM_ORE_ESE"]) if str(row["NUM_ORE_ESE"]) != "nan" else 0
    n_practice_groups = int(row["NUM_SQU_ESE"]) if str(row["NUM_SQU_ESE"]) != "nan" else 0
    if practice_hours != 0:
        n_min_double_slots_practice = \
            practice_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_ESERCITAZIONE"])][0]
        n_min_single_slots_practice = \
            practice_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_ESERCITAZIONE"])][1]
    else:
        n_min_double_slots_practice = 0
        n_min_single_slots_practice = 0

    return practice_hours, n_practice_groups, n_min_double_slots_practice, n_min_single_slots_practice

'''
    Get Lab organization preferences from the Excel file
'''
def get_lab_preferences(row):
    lab_hours = int(row["NUM_ORE_LAB"]) if str(row["NUM_ORE_LAB"]) != "nan" else 0
    n_lab_groups = int(row["NUM_SQU_LAB"]) if str(row["NUM_SQU_LAB"]) != "nan" else 0
    if lab_hours != 0:
        if str(row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) != "nan":
            n_blocks_lab = int(row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) if str(
                row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) != "nan" else 0
            n_weekly_groups_lab = int(row["NUM_SQUADRE_SETTIMANALI_LAIB_ATENEO"]) if str(
                row["NUM_SQUADRE_SETTIMANALI_LAIB_ATENEO"]) != "nan" else 0
            double_slots_lab = lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAIB_ATENEO"])]
        else:
            n_blocks_lab = int(row["NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE"]) if str(
                row["NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE"]) != "nan" else 0
            n_weekly_groups_lab = int(row["NUM_SQUADRE_SETTIMANALI_LAB_DIPARTIMENTALE"]) if str(
                row["NUM_SQUADRE_SETTIMANALI_LAB_DIPARTIMENTALE"]) != "nan" else 0
            double_slots_lab = \
                lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAB_DIPARTIMENTALE"])]
    else:
        n_blocks_lab = 0
        n_weekly_groups_lab = 0
        double_slots_lab = 0

    return lab_hours, n_lab_groups, n_blocks_lab, n_weekly_groups_lab, double_slots_lab

'''
    Get Lecture organization preferences from the Excel file
'''
def get_teachers_preferences(teachings):
    db_api = DbApi()

    preferences_files = glob.glob(os.path.join("../Data/Excels/Teachers Data/Teachers Preferences", "*.xlsx"))

    for f in preferences_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)

        # Converting the column with Teachers' IDs to string (it would be considered float otherwise)
        df["MATRICOLA_TITOLARE"] = df["MATRICOLA_TITOLARE"].astype(str)

        # Filtering by Course name and Main Teacher's name, since we do not have the id_inc in the Teachers preferences files
        filtered_df = df.loc[df["TITOLO_MATERIA"].str.lower().isin([t.title.lower() for t in teachings]) &
                             df["MATRICOLA_TITOLARE"].str.zfill(6).isin([t.main_teacher for t in teachings])]

        for index, row in filtered_df.iterrows():
            # Lectures
            n_min_double_slots_lecture = lecture_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LEZIONE"])][0]
            n_min_single_slots_lecture = lecture_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LEZIONE"])][1]

            # Practices
            practice_hours, n_practice_groups, n_min_double_slots_practice, n_min_single_slots_practice = get_practice_preferences(row)

            # Labs
            lab_hours, n_lab_groups, n_blocks_lab, n_weekly_groups_lab, double_slots_lab = get_lab_preferences(row)

            # Insert the data retrieved from the Excel files in the DB
            db_api.insert_teaching_preference(
                row["TITOLO_MATERIA"],
                row["MATRICOLA_TITOLARE"].zfill(6),
                n_min_double_slots_lecture,
                n_min_single_slots_lecture,
                practice_hours,
                n_practice_groups,
                n_min_double_slots_practice,
                n_min_single_slots_practice,
                lab_hours,
                n_lab_groups,
                n_blocks_lab,
                n_weekly_groups_lab,
                double_slots_lab
            )

    print("Teachers preferences inserted in the DB")

'''
    Get Teacher's unavailabilities from the file PreferenzeDocenti.xlsx
'''
def get_teachers_unavailabilities():
    db_api = DbApi()

    # Support vectors needed to find the index of the Day and the Slot
    days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"]
    slots = ["08:30", "10:00", "11:30", "13:00", "14:30", "16:00", "17:30"]

    df = pandas.read_excel("../Data/Excels/Teachers Data/Teachers Preferences/PreferenzeDocenti.xlsx")
    db_api.clear_teachers_unavailabilities()
    for index, row in df.iterrows():
        teacher_id = str(row['MATRICOLA_TITOLARE']).zfill(6)

        result = db_api.check_teacher_id(teacher_id)

        if result and str(row["INDISPONIBILITA_SETTIMANALI"]) != 'nan':
            unavailabilities_list = str(row["INDISPONIBILITA_SETTIMANALI"]).split(',')
            for i in range(0, min(len(unavailabilities_list), 4)):
                unavailability = unavailabilities_list[i].split(' ')

                # unavailability[0] contains the Day in format "Lunedì", "Martedì", etc. - unavailability[1] cointains the Slot in format "08:30", "10:00", etc.
                db_api.insert_unavailable_slot(teacher_id, (days.index(unavailability[0]) * 7) + slots.index(unavailability[1]))

    print("Teachers unavailabilities inserted in the DB")