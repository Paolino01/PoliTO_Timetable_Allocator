'''This class contains all the parameters of the program (e.g. number of slots per day, is saturday enabled, etc.). These parameters will be used in the generation of the timetable.'''
class Parameters:
    def __init__(self):
        # DB created by the Scraper
        self.DB = "../Scraper_Tesi/Data/GoodDB.db"

        # Number of lecture slots per each day, 5 days per week
        self.slotPerDay: int = 7

        #Boolean variable that tells if we can allocate lectures on Saturday or not. Default is false
        self.saturdayEnabled: bool = False
        #Saves the number of slots on Saturday. Minimum is 1, maximum is 7, default is 4
        self.nSlotsSaturday: int = 4

    def setSaturdayEnabled(self, saturdayEnabled: bool):
        self.saturdayEnabled = saturdayEnabled

    def setNSlotsSaturday(self, nSlotsSaturday: int):
        self.nSlotsSaturday = nSlotsSaturday