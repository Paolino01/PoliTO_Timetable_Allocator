import glob
import math
import os
import pandas

from Data.Db_API import Db_API

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
    "nan": [0, 0]
}

lab_slot_preferences_dict = {
    "blocchi da 3h per ciascuna squadra": [1, 0],
    "blocchi da 1,5h per ciascuna squadra": [0, 1],
    "indifferente": [0, 0],
    "nan": [0, 0]
}

def get_teachers_preferences(teachings):
    db_api = Db_API()

    preferences_files = glob.glob(os.path.join("../Data/Excels/Teachers Data/Teachers Preferences", "*.xls"))

    for f in preferences_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)

        # Filtering by Course name and Main Teacher's name, since we do not have the id_inc in the Teachers preferences files
        filtered_df = df.loc[df["TITOLO_MATERIA"].str.lower().isin([t.title.lower() for t in teachings]) & df[
            "DOCENTE_TITOLARE"].str.lower().isin([t.main_teacher.lower() for t in teachings])]

        for index, row in filtered_df.iterrows():
            # Lectures
            n_min_double_slots_lecture = lecture_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LEZIONE"])][0]
            n_min_single_slots_lecture = lecture_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LEZIONE"])][1]

            # Practices
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

            # Labs
            lab_hours = int(row["NUM_ORE_LAB"]) if str(row["NUM_ORE_LAB"]) != "nan" else 0
            n_lab_groups = int(row["NUM_SQU_LAB"]) if str(row["NUM_SQU_LAB"]) != "nan" else 0
            if lab_hours != 0:
                if str(row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) != "nan":
                    n_blocks_lab = int(row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) if str(
                        row["NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO"]) != "nan" else 0
                    n_weekly_groups_lab = int(row["NUM_SQUADRE_SETTIMANALI_LAIB_ATENEO"]) if str(
                        row["NUM_SQUADRE_SETTIMANALI_LAIB_ATENEO"]) != "nan" else 0
                    n_min_double_slots_lab = lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAIB_ATENEO"])][
                        0]
                    n_min_single_slots_lab = lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAIB_ATENEO"])][
                        1]
                else:
                    n_blocks_lab = int(row["NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE"]) if str(
                        row["NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE"]) != "nan" else 0
                    n_weekly_groups_lab = int(row["NUM_SQUADRE_SETTIMANALI_LAB_DIPARTIMENTALE"]) if str(
                        row["NUM_SQUADRE_SETTIMANALI_LAB_DIPARTIMENTALE"]) != "nan" else 0
                    n_min_double_slots_lab = \
                    lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAB_DIPARTIMENTALE"])][0]
                    n_min_single_slots_lab = \
                    lab_slot_preferences_dict[str(row["ORGANIZZAZIONE_BLOCCHI_LAB_DIPARTIMENTALE"])][1]
            else:
                n_blocks_lab = 0
                n_weekly_groups_lab = 0
                n_min_double_slots_lab = 0
                n_min_single_slots_lab = 0

            # Insert the data retrieved from the Excel files in the DB
            db_api.insert_teaching_preference(
                row["TITOLO_MATERIA"],
                row["DOCENTE_TITOLARE"],
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
                n_min_double_slots_lab,
                n_min_single_slots_lab,
            )

    print("Teachers preferences inserted in the DB")


def get_teachers_unavailabilities():
    db_api = Db_API()

    df = pandas.read_excel("../Data/Excels/Teachers Data/JOTFORM.xlsx")
    db_api.clear_teachers_unavailabilities()
    for i in df.index:
        teacher = df.loc[i]['Docente titolare']

        # I have to do it like this because the data in the JotForm is in the format:
        # 8:30-10:00 Monday; 8:30-10:00 Tuesday; 8:30-10:00 Wednesday; ...; 10:00-11:30 Monday; 10:00-11:30 Tuesday; ...; 17:30-19:00 Thursday; 17:30-19:00 Friday
        for day in range(5, 10):
            for slot in range(0, 35, 5):
                if df.iloc[i, day + slot] == "Indisponibile" or df.iloc[i, day + slot] == "Unavailable":
                    db_api.insert_unavailable_slot(teacher, ((day - 5) * 7) + math.floor(slot / 5))

    print("Teachers unavailabilities inserted in the DB")