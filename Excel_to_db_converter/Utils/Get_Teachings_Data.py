import glob
import os
import pandas

from Data.Db_API import Db_API


def get_lecture_hours(teachings):
    db_api = Db_API()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    for f in courses_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)
        filtered_df = df.loc[df["id_inc"].isin([t.id_teaching for t in teachings])]
        for index, row in filtered_df.iterrows():
            # Adding the information about hours of lectures to a Teaching
            db_api.add_lecture_hours_to_course(row["id_inc"], row["h_lez"])

    print("Lecture hours inserted in the DB")