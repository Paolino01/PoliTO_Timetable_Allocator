import math
import pandas
import glob
import os

from Data.Db_API import Db_API

'''
    Given a practice/lab lecture in format "Type hours*#teachers*#slots", returns the total number of hours for that lecture.
'''
def split_slot_hours(slot):
    slot_hours = slot.split()
    if slot_hours[0] != '0' and len(slot_hours) == 2:
        slot_hours = slot_hours[1].split('*')
        slot_hours = float(slot_hours[0].replace(",", ".")) * int(slot_hours[2])
    else:
        slot_hours = 0

    return slot_hours

'''
    Given a Teaching, returns the total number of hours for lectures of that course.
'''
def calculate_lecture_hours_for_course(row):
    practice_hours = split_slot_hours(row["h_ese"])
    return float(row["h_lez"]) + practice_hours

if __name__ == '__main__':
    db_api = Db_API()

    '''
    Teachings
    Get the Teachings information from the Excel files and insert them in the database 
    '''

    # Load the Teaching IDs from the DB
    list_teachings_ids = db_api.get_teachings_ids()

    # Converting the data in the list
    list_teachings_ids = [t[0] for t in list_teachings_ids]

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    for f in courses_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)
        filtered_df = df.loc[df["id_inc"].isin(list_teachings_ids)]
        for index, row in filtered_df.iterrows():
            # Retrieving the information about hours of lectures and laboratories for each Teaching
            lecture_hours = calculate_lecture_hours_for_course(row)
            lab_hours = split_slot_hours(row["h_lab"])

            # Adding the information about hours of lectures and laboratories to a Teaching
            db_api.add_lecture_hours_to_course(row["id_inc"], lecture_hours, lab_hours)

    print("Teachings hours inserted in the DB")



    '''
    Teachers
    Get the information about unavailable Slots for each Teacher from the JotForm Excel file and insert them in the database
    '''

    df = pandas.read_excel("../Data/Excels/Teachers Data/JOTFORM.xlsx")
    db_api.clear_teachers_unavailabilities()
    for i in df.index:
        teacher = df.loc[i]['Docente titolare']

        # I have to do it like this because the data in the JotForm is in the format:
        # 8:30-10:00 Monday; 8:30-10:00 Tuesday; 8:30-10:00 Wednesday; ...; 10:00-11:30 Monday; 10:00-11:30 Tuesday; ...; 17:30-19:00 Thursday; 17:30-19:00 Friday
        for day in range(5, 10):
            for slot in range(0, 35, 5):
                if df.iloc[i, day+slot] == "Indisponibile" or df.iloc[i, day+slot] == "Unavailable":
                    db_api.insert_unavailable_slot(teacher, ((day-5)*7) + math.floor(slot/5))

    print("Teachers unavailabilities inserted in the DB")