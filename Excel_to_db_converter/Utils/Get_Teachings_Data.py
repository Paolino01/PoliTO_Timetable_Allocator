import glob
import os
import pandas

from Data.Db_API import Db_API

'''
    Get the information about the teachers, they hours, and the type of their lectures for each Teaching, using the column "Collaboratori" (Collaborators)
    Collaborators are in the format: (ID) NAME (SOMETHING) DEPARTMENT tit: TITLE tipo did:LECTURE_TYPE lin:LANGUAGE - h:  hh.mm;
    PAY ATTENTION TO THE SPACES, SOME FIELDS HAVE SPACES OTHER DON'T. After "h:" there is a double space
    I'm interested only to the teachers who have tit=IN
'''
def get_teaching_teachers(row, main_teacher):
    collaborators_string = row['Collaboratori']
    if collaborators_string == "" or collaborators_string == "No coll.":
        return

    # TODO: need to find a way to retrieve the Teachers from their surnames/IDs (there are multiple Teachers with the same surname)
    '''
    db_api = Db_API()

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
                    
        # Considering only the Teachers who have title = "IN" and didactic type = "L", "EA" or "EL"
        # Or the Main Teacher independently of the title
        if main_teacher.split(' ')[0].upper() == coll_info[1].upper():
            if coll_info[7 + offset].split(":")[1] == "L":
                db_api.add_teacher_hours(main_teacher, coll_info[12 + offset], "L", row["id_inc"])
            else:
                if coll_info[7 + offset].split(":")[1] in ("EA", "EL"):
                    db_api.add_teacher_in_teaching(coll_info[1], coll_info[12 + offset], coll_info[7 + offset].split(":")[1], row["id_inc"])
        else:
            if coll_info[5 + offset] == "IN" and coll_info[7 + offset].split(":")[1] in ("L", "EA", "EL"):
                db_api.add_teacher_in_teaching(coll_info[1], coll_info[12 + offset], coll_info[7 + offset].split(":")[1], row["id_inc"])
    '''


def get_teaching_information(teachings):
    db_api = Db_API()

    # Get all the Excel files in the "Courses Data" folder
    courses_files = glob.glob(os.path.join("../Data/Excels/Courses Data", "*.xls"))

    db_api.delete_teacher_in_teaching()

    for f in courses_files:
        # For each file, getting only the courses that are in the DB
        df = pandas.read_excel(f)
        filtered_df = df.loc[df["id_inc"].isin([t.id_teaching for t in teachings])]

        for index, row in filtered_df.iterrows():
            # Getting the main teacher's name for a Teaching
            main_teacher = row["cognome"] + " " + row["nome"]
            main_teacher = main_teacher.title()
            # Adding the information about hours of lectures to a Teaching
            db_api.add_teacher_and_lecture_hours_to_course(row["id_inc"], row["h_lez"], main_teacher)

            get_teaching_teachers(row, main_teacher)

    print("Lecture and Teachers hours inserted in the DB")