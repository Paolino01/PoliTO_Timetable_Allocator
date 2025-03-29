import pandas
import glob
import os

from Data.Db_API import Db_API

if __name__ == '__main__':
    db_api = Db_API()

    # Load the Teaching IDs from the DB
    list_teachings_names = db_api.get_teachings_names()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Courses Data", "*.xls"))

    for f in courses_files:
        df = pandas.read_excel(f)
        print(df["id_inc"].isin(list_teachings_names))