from Utils.Components.Teaching import Teaching


class Teacher:
    def __init__(self, teacher_name: str, teacher_id: str):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.teachings: list[Teaching] = []
        self.unaivalable_slots = []

    def add_teachings(self, teaching_id: str, all_teachings: list[Teaching]):
        teaching = [t for t in all_teachings if t.id_teaching == teaching_id]
        if len(teaching) > 0:
            self.teachings.append(teaching[0])

    def add_unaivalable_slots(self, unaivalable_slot: int):
        self.unaivalable_slots.append(unaivalable_slot)