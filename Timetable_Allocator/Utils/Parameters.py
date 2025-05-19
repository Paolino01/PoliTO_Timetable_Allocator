'''This class contains all the parameters of the program (e.g. number of slots per day, is saturday enabled, etc.). These parameters will be used in the generation of the timetable.'''
class Parameters:
    def __init__(self):
        # DB witth the information about the courses
        self.DB = "../Data/Courses_DB.db"

        # Data structure that is used to decide the order of the courses when generating a timetable
        self.course_order = [
            {
                "courses": [
                    "ICT ENGINEERING FOR SMART SOCIETIES"
                    "ICT FOR SMART SOCIETIES (ICT PER LA SOCIETA' DEL FUTURO)",
                    "DATA SCIENCE AND ENGINEERING",
                    "ELECTRONIC AND COMMUNICATIONS ENGINEERING (INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI)",
                    "INGEGNERIA ELETTRONICA",
                    "COMMUNICATIONS AND COMPUTER NETWORKS ENGINEERING (INGEGNERIA TELEMATICA E DELLE COMUNICAZIONI)",
                    "CYBERSECURITY",
                    "CYBERSECURITY ENGINEERING",
                    "MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA)",
                    "NANOTECHNOLOGIES FOR ICTs (NANOTECNOLOGIE PER LE ICT)",
                    "INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE",
                    "INGEGNERIA DEL CINEMA E DEI MEDIA DIGITALI",
                    "INGEGNERIA FISICA",
                    "PHYSICS OF COMPLEX SYSTEMS (FISICA DEI SISTEMI COMPLESSI)",
                    "COMMUNICATIONS ENGINEERING",
                    "INGEGNERIA ELETTRONICA (ELECTRONIC ENGINEERING)",
                    "QUANTUM ENGINEERING",
                    "AGRITECH ENGINEERING"
                ],
                "orientations": [],
                "course_type": "",
                "max_corr_in_day": 500,
                "max_corr_first_last_slot": 0,
                "min_corr_overlaps": 20
            },
            {
                "courses": ["INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)"],
                "orientations": ["Artificial Intelligence and Data Analytics",
                                 "Automation and Intelligent Cyber-Physical Systems",
                                 "Bio and Health Informatics", "Computer Networks and Cloud Computing",
                                 "Computing and Network Infrastructures", "EMECS - Path 1", "EMECS - Path 2", "ESCP",
                                 "Embedded systems"],
                "course_type": "Z",
                "max_corr_in_day": 700,
                "max_corr_first_last_slot": 0,
                "min_corr_overlaps": 20
            },
            {
                "courses": ["INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)"],
                "orientations": ["Software", "Grafica e Multimedia"],
                "course_type": "Z",
                "max_corr_in_day": 700,
                "max_corr_first_last_slot": 20,
                "min_corr_overlaps": 20
            },
            {
                "courses": ["INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)"],
                "orientations": [],
                "course_type": "1",
                "max_corr_in_day": 700,
                "max_corr_first_last_slot": 20,
                "min_corr_overlaps": 20
            },
            {
                "courses": ["INGEGNERIA INFORMATICA"],
                "orientations": [],
                "course_type": "1",
                "max_corr_in_day": 800,
                "max_corr_first_last_slot": 20,
                "min_corr_overlaps": 20
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

        # Number of maximum consecutive Slots in a day for a Teaching
        self.max_consecutive_slots_teaching = 2

        # Number of maximum consecutive slots for a Teacher
        self.max_consecutive_slots_teacher = 4

        # Penalties for soft contraints
        self.teaching_overlaps_penalty = 80
        self.lecture_dispersion_penalty = 50
        self.correlation_in_day_penalty = 20

        # Name of the timetable saved in the DB
        self.timetable_name = "All courses timetable"

        # Name of day and time slot
        self.days = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        self.time_slots = ["8.30-10.00", "10.00-11.30", "11.30-13.00", "13.00-14.30", "14.30-16.00", "16.00-17.30", "17.30-19.00"]

    def set_saturday_enabled(self, saturday_enabled: bool):
        self.saturday_enabled = saturday_enabled

    def set_n_slots_saturday(self, n_slots_saturday: int):
        self.n_slots_saturday = n_slots_saturday
