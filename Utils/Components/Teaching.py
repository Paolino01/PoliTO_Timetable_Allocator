class Teaching:
    '''It contains the data of a Teaching taken from the database'''

    def __init__(self, id_teaching: str, n_students: int, n_students_freq: int, college: str, title: str, cfu: int, hours_lect: int,
                 main_teacher: str):
        self.id_teaching: str = id_teaching
        self.n_students: int = n_students
        self.n_students_freq: int = n_students_freq
        self.college: str = college
        self.title: str = title
        self.cfu: int = cfu
        self.hours_lect: int = hours_lect
        self.main_teacher: str = main_teacher

        # Correlations between teachings. I have a dictionary where the key is a teaching and the value is the weight of the correlation for that teaching
        # As default I set the correlation of a Teaching with itself to 100
        self.correlations: dict = {id_teaching: 100}

    def set_correlations(self, id_teaching: str, correlation: int):
        self.correlations[id_teaching] = correlation