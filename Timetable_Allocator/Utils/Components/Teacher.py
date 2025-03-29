class Teacher:
    def __init__(self, surname):
        self.surname = surname
        self.teachings_ids = []

    def add_teachings(self, teachings_ids):
        self.teachings_ids.append(teachings_ids)