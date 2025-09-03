class Teaching:
    '''It contains the data of a Teaching taken from the database'''

    def __init__(
        self,
        id_teaching: str,
        title: str,
        cfu: int,
        main_teacher_id: str,
        didactic_period: str,

        lect_slots: int,
        n_min_double_slots_lecture,
        n_min_single_slots_lecture,

        practice_slots: int,
        n_practice_groups: int,
        n_min_double_slots_practice: int,
        n_min_single_slots_practice: int,

        lab_slots: int,
        n_lab_groups: int,
        n_blocks_lab: int,
        double_slots_lab: int
    ):
        self.id_teaching: str = id_teaching
        self.title: str = title
        self.cfu: int = cfu
        self.main_teacher_id: str = main_teacher_id
        self.didactic_period: str = didactic_period

        self.lect_slots: int = lect_slots
        self.n_min_double_slots_lecture: int = n_min_double_slots_lecture
        self.n_min_single_slots_lecture: int = n_min_single_slots_lecture

        self.practice_slots: int = practice_slots
        self.n_practice_groups: int = n_practice_groups
        self.n_min_double_slots_practice: int = n_min_double_slots_practice
        self.n_min_single_slots_practice: int = n_min_single_slots_practice

        self.lab_slots: int = lab_slots
        self.n_lab_groups: int = n_lab_groups
        self.n_blocks_lab: int = n_blocks_lab
        self.double_slots_lab: int = double_slots_lab

        # Correlations between teachings. I have a dictionary where the key is a teaching and the value is the weight of the correlation for that teaching
        # As default I set the correlation of a Teaching with itself to 100
        self.correlations: dict = {self: (100, True)}

    '''
        Set the correlations between the teachings. Mandatory is True if one of the Teachings is "Obbligatorio"
    '''
    def set_correlations(self, teaching, correlation: int, mandatory: bool = False):
        self.correlations[teaching] = (correlation, mandatory)