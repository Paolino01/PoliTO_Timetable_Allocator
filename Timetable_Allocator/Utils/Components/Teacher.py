class Teacher:
    def __init__(self, surname):
        self.surname = surname
        self.teachings_ids = []
        self.unaivalable_slots = []

    def add_teachings(self, teachings_ids: str):
        self.teachings_ids.append(teachings_ids)

    def add_unaivalable_slots(self, unaivalable_slot: int):
        self.unaivalable_slots.append(unaivalable_slot)