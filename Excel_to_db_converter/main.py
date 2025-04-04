from Data.Db_API import Db_API
from Utils.Get_Teachers_Data import get_teachers_preferences, get_teachers_unavailabilities
from Utils.Get_Teachings_Data import get_lecture_hours
from Utils.Teaching import Teaching

if __name__ == '__main__':
    db_api = Db_API()

    # Load the Teaching IDs from the DB
    list_teachings_ids = db_api.get_teachings()
    teachings = []

    # Converting the data in the list
    for row in list_teachings_ids:
        teachings.append(Teaching(id_teaching=row[0], title=row[1], main_teacher=row[2]))

    '''Teachings'''
    # Get the number of lecture hours from the Excel files and insert it in the database
    get_lecture_hours(teachings)


    '''Teachers'''
    # Get the Teachers preferences for the courses and save them in the database
    get_teachers_preferences(teachings)

    # Get the information about unavailable Slots for each Teacher from the JotForm Excel file and insert them in the database
    get_teachers_unavailabilities()