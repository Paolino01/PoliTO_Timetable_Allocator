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
    '''
    list_teachings_names = db_api.get_teachings_names()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    for f in courses_files:
        df = pandas.read_excel(f)
        print(df["id_inc"].isin(list_teachings_names))
    '''

    '''
    Teachers
    Get the Teachers information from the JotForm Excel file and insert them in the database
    '''

    df = pandas.read_excel("../Data/Excels/Teachers Data/JOTFORM.xlsx")
    for i in df.index:
        teacher = df.loc[i]['Docente titolare']
        for slot in range(0, 7):
            for day in range(5, 40, 7):
                if df.iloc[i, day+slot] == "Indisponibile" or df.iloc[i, day+slot] == "Unaivalable":
                    print(df.iloc[i, day+slot])