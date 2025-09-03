from Timetable_Allocator.DB_Connection.DbAPI import DbAPI
from Timetable_Allocator.Components.Models.Teacher import Teacher
from Timetable_Allocator.Components.Models.Teaching import Teaching


class Teachers:
    def __init__(self, all_teachings:list[Teaching], params):
        self.teachers_list:list[Teacher] = []
        self.db_api = DbAPI(params)

        self.load_teachers_from_db()
        self.load_teachings_for_teacher(all_teachings)
        self.load_unaivalable_slots()

    ''' Load all the teachers from the db, by surname. '''
    def load_teachers_from_db(self):
        list_teachers = self.db_api.get_teachers()

        for row in list_teachers:
            self.teachers_list.append(Teacher( str(row[0]), str(row[1]) ))

    ''' Load the Teachings of a Teacher from the DB '''
    def load_teachings_for_teacher(self, all_teachings:list[Teaching]):
        for teacher in self.teachers_list:
            list_teachings_for_teacher = self.db_api.get_teachings_for_teacher(teacher.teacher_id)

            for row in list_teachings_for_teacher:
                teacher.add_teachings(str(row[0]), str(row[1]), all_teachings)

    ''' Load the unaivalable slots for a Teacher '''
    def load_unaivalable_slots(self):
        for teacher in self.teachers_list:
            list_unavalable_slots = self.db_api.get_teachers_unavailabilities(teacher.teacher_id)

            for row in list_unavalable_slots:
                teacher.add_unaivalable_slots(int(row[0]))