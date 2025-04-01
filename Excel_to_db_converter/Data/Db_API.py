import sqlite3

class Db_API:
    def __init__(self):
        self.db = sqlite3.connect("../Data/Courses_DB.db")

    '''
        Get all the teachings in the DB
        Return: list of teachings in format [titolo]
    '''
    def get_teachings_ids(self):
        cur = self.db.cursor()
        sql = "SELECT ID_INC FROM Insegnamento WHERE ID_INC IN (SELECT ID_INC FROM Insegnamento_in_Orientamento WHERE orientamento = 'MECHATRONIC ENGINEERING (')"
        cur.execute(sql)
        teachings_ids = cur.fetchall()
        return teachings_ids

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