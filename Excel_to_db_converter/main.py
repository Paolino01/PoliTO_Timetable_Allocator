from Data.DbApi import DbApi
from Utils.Get_Teachers_Data import get_teachers_preferences, get_teachers_unavailabilities
from Utils.Get_Teachings_Data import get_teaching_information, get_teachings, calculate_correlations
from Utils.Teaching import Teaching

if __name__ == '__main__':
    db_api = DbApi()

    # Load the Teachings from the DB
    list_teachings = db_api.get_teachings()
    teachings = []

    # Converting the data in the list
    for row in list_teachings:
        teachings.append(Teaching(id_teaching=row[0], title=row[1], main_teacher=row[2]))

    '''Teachings'''
    # Get the Degree Courses related to DAUIN and DET departments (IDs CL003 and CL006)
    get_teachings()
    # Calculate the correlation for each Teaching
    calculate_correlations()

    # Get the number of lecture hours from the Excel files and insert it in the database
    get_teaching_information(teachings)


    '''Teachers'''
    # Get the Teachers preferences for the courses and save them in the database
    get_teachers_preferences(teachings)

    # Get the information about unavailable Slots for each Teacher from the JotForm Excel file and insert them in the database
    get_teachers_unavailabilities()
