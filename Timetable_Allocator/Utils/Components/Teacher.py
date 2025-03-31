from Utils.Components.Teaching import Teaching


class Teacher:
    def __init__(self, teacher:str):
        self.teacher = teacher
        self.teachings: list[Teaching] = []
        self.unaivalable_slots = []

    def add_teachings(self, teaching_id: str, all_teachings: list[Teaching]):
        self.teachings.append(next((t for t in all_teachings if t.id_teaching == teaching_id)))

    def add_unaivalable_slots(self, unaivalable_slot: int):
        self.unaivalable_slots.append(unaivalable_slot)