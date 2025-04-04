class Teaching:
    '''It contains the data of a Teaching taken from the database'''

    def __init__(self, id_teaching: str, title: str, main_teacher: str):
        self.id_teaching: str = id_teaching
        self.title: str = title
        self.main_teacher: str = main_teacher