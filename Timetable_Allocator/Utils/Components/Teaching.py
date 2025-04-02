class Teaching:
    '''It contains the data of a Teaching taken from the database'''

    def __init__(self, id_teaching: str, title: str, cfu: int, lect_hours: int,
                 lab_hours: int, main_teacher: str, didactic_period: str):
        self.id_teaching: str = id_teaching
        self.title: str = title
        self.cfu: int = cfu
        self.lect_hours: int = lect_hours
        self.lab_hours = lab_hours
        self.main_teacher: str = main_teacher
        self.didactic_period: str = didactic_period

        # Correlations between teachings. I have a dictionary where the key is a teaching and the value is the weight of the correlation for that teaching
        # As default I set the correlation of a Teaching with itself to 100
        self.correlations: dict = {id_teaching: 100}

    def set_correlations(self, id_teaching: str, correlation: int):
        self.correlations[id_teaching] = correlation