'''This class contains all the parameters of the program (e.g. number of slots per day, is saturday enabled, etc.). These parameters will be used in the generation of the timetable.'''
class Parameters:
    def __init__(self):
        # DB created by the Scraper
        self.DB = "../Data/Courses_DB.db"

        # Number of lecture Slots per each day, 5 days per week
        self.slot_per_day: int = 7
        # Number of weeks in a semester
        self.n_weeks_in_semester = 14
        # Number of hours that are in a slot
        self.hours_in_slot = 1.5

        # Boolean variable that tells if we start from an existing solution or not
        self.start_from_previous_solution = False
        # Boolean variable that tells if we can allocate lectures on Saturday or not. Default is false
        self.saturday_enabled: bool = False
        # Saves the number of slots on Saturday. Minimum is 1, maximum is 7, default is 4
        self.n_slots_saturday: int = 4

        # Number of maximum correlated lectures in a day
        self.max_corr_in_day = 700
        # Number of consecutive slots on which we calculate the minimum correlated lectures
        self.n_consecutive_slots = 3
        # Number of minimum correlated lectures in self.n_consecutive_slots slots
        self.min_corr_in_slots = 0
        # Number of maximum correlation value between first and last slot of a day
        self.max_corr_first_last_slot = 100
        # Minimum correlation for which overlaps must be avoided
        self.min_corr_overlaps = 30

        # Number of maximum consecutive Slots in a day for a Teaching
        self.max_consecutive_slots_teaching = 2

        # Number of maximum consecutive slots for a Teacher
        self.max_consecutive_slots_teacher = 4

        # Penalties for soft contraints
        self.teaching_overlaps_penalty = 100
        self.lecture_dispersion_penalty = 20

        # Name of day and time slot
        self.days = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        self.time_slots = ["8.30-10.00", "10.00-11.30", "11.30-13.00", "13.00-14.30", "14.30-16.00", "16.00-17.30", "17.30-19.00"]

    def set_saturday_enabled(self, saturday_enabled: bool):
        self.saturday_enabled = saturday_enabled

    def set_n_slots_saturday(self, n_slots_saturday: int):
        self.n_slots_saturday = n_slots_saturday
