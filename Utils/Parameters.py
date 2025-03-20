'''This class contains all the parameters of the program (e.g. number of slots per day, is saturday enabled, etc.). These parameters will be used in the generation of the timetable.'''
class Parameters:
    def __init__(self):
        # DB created by the Scraper
        self.DB = "../Scraper_Tesi/Data/GoodDB.db"

        # Number of lecture Slots per each day, 5 days per week
        self.slot_per_day: int = 7

        #Boolean variable that tells if we can allocate lectures on Saturday or not. Default is false
        self.saturday_enabled: bool = False
        #Saves the number of slots on Saturday. Minimum is 1, maximum is 7, default is 4
        self.n_slots_saturday: int = 4

        # Number of maximum consecutive lecture Slots that students can have in a day
        self.max_consecutive_slots = 4

    def set_saturday_enabled(self, saturday_enabled: bool):
        self.saturday_enabled = saturday_enabled

    def set_n_slots_saturday(self, n_slots_saturday: int):
        self.n_slots_saturday = n_slots_saturday