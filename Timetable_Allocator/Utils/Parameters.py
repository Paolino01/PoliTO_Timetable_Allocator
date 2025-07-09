'''This class contains all the parameters of the program (e.g. number of slots per day, is saturday enabled, etc.). These parameters will be used in the generation of the timetable.'''
class Parameters:
    def __init__(self):
        # DB witth the information about the courses
        self.DB = "../Data/Courses_DB.db"

        # Data structure that is used to decide the order of the courses when generating a timetable
        self.course_order = [
            {
                "courses": [
                    "ELECTRONIC AND COMMUNICATIONS ENGINEERING (INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI)",
                    "INGEGNERIA FISICA",
                    "AGRITECH ENGINEERING",
                    "COMMUNICATIONS ENGINEERING",
                    "ICT FOR SMART SOCIETIES (ICT PER LA SOCIETA' DEL FUTURO)",
                    "NANOTECHNOLOGIES FOR ICTs (NANOTECNOLOGIE PER LE ICT)",
                    "PHYSICS OF COMPLEX SYSTEMS(FISICA DEI SISTEMI COMPLESSI)",
                    "QUANTUM ENGINEERING",
                    "ICT ENGINEERING FOR SMART SOCIETIES",
                    "INGEGNERIA ELETTRONICA (ELECTRONIC ENGINEERING)"
                ],
                "orientations": [],
                "course_type": "",
                "max_corr_in_day": 700,
                "max_corr_first_last_slot": 20,
                "min_corr_overlaps": 20,
                "no_overlap_mandatory_practice_lab": True,
                "no_overlap_groups": True,
                "teachers_unavailabilities": True
            },
            {
                "courses": [
                    "INGEGNERIA ELETTRONICA",
                ],
                "orientations": [],
                "course_type": "",
                "max_corr_in_day": 900,
                "max_corr_first_last_slot": 30,
                "min_corr_overlaps": 35,
                "no_overlap_mandatory_practice_lab": False,
                "no_overlap_groups": False,
                "teachers_unavailabilities": False
            }
        ]

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
        self.max_corr_in_day = 800
        # Number of maximum correlation value between first and last slot of a day
        self.max_corr_first_last_slot = 20
        # Minimum correlation for which overlaps must be avoided
        self.min_corr_overlaps = 20
        # True if Practices and Labs of mandatory courses should not overlap with non mandatory courses
        self.no_overlap_mandatory_practice_lab = True
        # True if I don't want to overlap different Practice/Lab groups of the same Teaching
        self.no_overlap_groups = True
        # True if I want to consider the Teachers' unavailabilities
        self.teachers_unavailabilities = True

        # Number of maximum consecutive Slots in a day for a Teaching
        self.max_consecutive_slots_teaching = 2

        # Penalties for soft contraints
        self.teaching_overlaps_penalty = 55
        self.lecture_dispersion_penalty = 25
        # This penalty should be negative since we are trying to maximize this parameter (and not minimize it)
        self.teacher_preferences_penalty = -10
        # This penalty should be negative since we are trying to maximize this parameter (and not minimize it)
        self.consecutive_groups_penalty = -10

        # Name of the timetable saved in the DB
        self.timetable_name = "ETF courses timetable"

        # Name of day and time slot
        self.days = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        self.time_slots = ["8.30-10.00", "10.00-11.30", "11.30-13.00", "13.00-14.30", "14.30-16.00", "16.00-17.30", "17.30-19.00"]

    def set_saturday_enabled(self, saturday_enabled: bool):
        self.saturday_enabled = saturday_enabled

    def set_n_slots_saturday(self, n_slots_saturday: int):
        self.n_slots_saturday = n_slots_saturday
