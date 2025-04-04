import sqlite3

class Db_API:
    def __init__(self):
        self.db = sqlite3.connect("../Data/Courses_DB.db")

    '''
        Get all the teachings in the DB
        Return: list of teachings in format [titolo]
    '''
    def get_teachings(self):
        cur = self.db.cursor()
        sql = "SELECT ID_INC,titolo, titolare FROM Insegnamento"
        cur.execute(sql)
        teachings_ids = cur.fetchall()
        return teachings_ids

    '''
        Update a Teaching in the DB with the hours of lectures
    '''
    def add_lecture_hours_to_course(self, id_inc, lecture_hours):
        cur = self.db.cursor()
        sql = "UPDATE Insegnamento SET oreLez = ? WHERE ID_INC = ?"
        cur.execute(sql, (lecture_hours, id_inc))
        self.db.commit()

    '''
        Update a Teaching in the DB with the info about organizations of lecture, practice, and lab hours
    '''
    def insert_teaching_preference(
            self,
            title,
            main_teacher,
            n_min_double_slots_lecture,
            n_min_single_slots_lecture,
            practice_hours,
            n_practice_groups,
            n_min_double_slots_practice,
            n_min_single_slots_practice,
            lab_hours,
            n_lab_groups,
            n_blocks_lab,
            n_weekly_groups_lab,
            n_min_double_slots_lab,
            n_min_single_slots_lab,
    ):
        cur = self.db.cursor()
        sql = ("UPDATE Insegnamento SET "
               "n_min_double_slots_lecture = ?,"
               "n_min_single_slots_lecture = ?,"
               "practice_hours = ?,"
               "n_practice_groups = ?,"
               "n_min_double_slots_practice = ?,"
               "n_min_single_slots_practice = ?,"
               "lab_hours = ?,"
               "n_lab_groups = ?,"
               "n_blocks_lab = ?,"
               "n_weekly_groups_lab = ?,"
               "n_min_double_slots_lab = ?,"
               "n_min_single_slots_lab = ?"
               "WHERE lower(titolo) = ? AND lower(titolare) = ?")

        cur.execute(sql, (
            n_min_double_slots_lecture,
            n_min_single_slots_lecture,
            practice_hours,
            n_practice_groups,
            n_min_double_slots_practice,
            n_min_single_slots_practice,
            lab_hours,
            n_lab_groups,
            n_blocks_lab,
            n_weekly_groups_lab,
            n_min_double_slots_lab,
            n_min_single_slots_lab,
            title.lower(),
            main_teacher.lower(),   # NOTE: the information about the main teacher is saved uppercase in the Excel file
        ))

        self.db.commit()

    '''
        Deletes all the Teachers_Unavailability entries    
    '''
    def clear_teachers_unavailabilities(self):
        cur = self.db.cursor()
        sql = "DELETE FROM Teachers_Unavailability"
        cur.execute(sql)
        self.db.commit()

    '''
        Insert an unavailable Slot for a Teacher
    '''
    def insert_unavailable_slot(self, teacher, slot):
        cur = self.db.cursor()

        # Check that the couple Teacher, Unavailable_Slot does not already exists in the database
        sql = "SELECT count(*) FROM Teachers_Unavailability WHERE Teacher = ? AND Unavailable_Slot = ?"
        cur.execute(sql, (teacher, slot))

        if cur.fetchone()[0] == 0:
            sql = "INSERT INTO Teachers_Unavailability VALUES (?, ?)"
            cur.execute(sql, (teacher, slot))
            self.db.commit()