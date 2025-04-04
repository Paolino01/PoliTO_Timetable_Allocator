class Teaching:
    '''It contains the data of a Teaching taken from the database'''

    def __init__(
        self,
        id_teaching: str,
        title: str,
        cfu: int,
        main_teacher: str,
        didactic_period: str,

        lect_hours: int,
        n_min_double_slots_lecture,
        n_min_single_slots_lecture,

        practice_hours: int,
        n_practice_groups: int,
        n_min_double_slots_practice: int,
        n_min_single_slots_practice: int,

        lab_hours: int,
        n_lab_groups: int,
        n_blocks_lab: int,
        n_weekly_groups_lab: int,
        n_min_double_slots_lab: int,
        n_min_single_slots_lab: int
    ):
        self.id_teaching: str = id_teaching
        self.title: str = title
        self.cfu: int = cfu
        self.main_teacher: str = main_teacher
        self.didactic_period: str = didactic_period

        self.lect_hours: int = lect_hours
        self.n_min_double_slots_lecture: int = n_min_double_slots_lecture
        self.n_min_single_slots_lecture: int = n_min_single_slots_lecture

        self.practice_hours: int = practice_hours
        self.n_practice_groups: int = n_practice_groups
        self.n_min_double_slots_practice: int = n_min_double_slots_practice
        self.n_min_single_slots_practice: int = n_min_single_slots_practice

        self.lab_hours: int = lab_hours
        self.n_lab_groups: int = n_lab_groups
        self.n_blocks_lab: int = n_blocks_lab
        self.n_weekly_groups_lab: int = n_weekly_groups_lab
        self.n_min_double_slots_lab: int = n_min_double_slots_lab
        self.n_min_single_slots_lab: int = n_min_single_slots_lab

        # Correlations between teachings. I have a dictionary where the key is a teaching and the value is the weight of the correlation for that teaching
        # As default I set the correlation of a Teaching with itself to 100
        self.correlations: dict = {id_teaching: 100}

    def set_correlations(self, id_teaching: str, correlation: int):
        self.correlations[id_teaching] = correlation