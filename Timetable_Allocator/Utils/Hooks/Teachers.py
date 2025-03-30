from Data.DbAPI import DbAPI
from Utils.Components.Teacher import Teacher


class Teachers:
    def __init__(self):
        self.teachers:list[Teacher] = []
        self.db_api = DbAPI()

        self.load_teachers_from_db()
        self.load_teachings_for_teacher()

    '''Load all the teachers from the db, by surname.'''
    def load_teachers_from_db(self):
        list_teachers_surnames = self.db_api.get_teachers_surnames()

        for row in list_teachers_surnames:
            self.teachers.append(Teacher(str(row[0])))

        print(self.teachers)

    def load_teachings_for_teacher(self):
        for t in self.teachers:
            list_teachings_for_teacher = self.db_api.get_teachings_for_teacher(t.surname)

            for row in list_teachings_for_teacher:
                t.add_teachings(str(row[0]))

    def load_unaivalable_slots(self):
        for t in self.teachers:
            list_unavalable_slots = self.db_api.get_unaivalable_slots(t.surname)

            for row in list_unavalable_slots:
                t.add_unaivalable_slots(int(row[0]))