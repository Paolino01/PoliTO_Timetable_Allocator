from Data.DbAPI import DbAPI
from Utils.Components.Teacher import Teacher
from Utils.Components.Teaching import Teaching


class Teachers:
    def __init__(self, all_teachings:list[Teaching], params):
        self.teachers_list:list[Teacher] = []
        self.db_api = DbAPI(params)

        self.load_teachers_from_db()
        self.load_teachings_for_teacher(all_teachings)
        self.load_unaivalable_slots()

    '''Load all the teachers from the db, by surname.'''
    def load_teachers_from_db(self):
        list_teachers = self.db_api.get_teachers()

        for row in list_teachers:
            self.teachers_list.append(Teacher( str(row[0]), str(row[1]) ))

    def load_teachings_for_teacher(self, all_teachings:list[Teaching]):
        for teacher in self.teachers_list:
            list_teachings_for_teacher = self.db_api.get_teachings_for_teacher(teacher.teacher_id)

            for row in list_teachings_for_teacher:
                teacher.add_teachings(str(row[0]), str(row[1]), all_teachings)

    def load_unaivalable_slots(self):
        for teacher in self.teachers_list:
            list_unavalable_slots = self.db_api.get_teachers_unavailabilities(teacher.teacher_id)

            for row in list_unavalable_slots:
                teacher.add_unaivalable_slots(int(row[0]))