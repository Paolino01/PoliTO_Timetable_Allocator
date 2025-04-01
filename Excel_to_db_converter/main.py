import math

import pandas
import glob
import os

from Data.Db_API import Db_API

if __name__ == '__main__':
    db_api = Db_API()

    '''
    Teachings
    Get the Teachings information from the Excel files and insert them in the database 
    '''

    # Load the Teaching IDs from the DB
    list_teachings_names = db_api.get_teachings_names()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    for f in courses_files:
        df = pandas.read_excel(f)
        print(df["id_inc"].isin(list_teachings_names))

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