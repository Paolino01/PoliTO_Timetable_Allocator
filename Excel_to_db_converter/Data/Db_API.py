import sqlite3

class Db_API:
    def __init__(self):
        self.db = sqlite3.connect("../Data/Courses_DB.db")

    '''Load all the teachings ids from the db.'''
    def get_teachings_names(self):
        cur = self.db.cursor()
        sql = "SELECT titolo FROM Insegnamento"
        cur.execute(sql)
        teachings_names = cur.fetchall()
        return teachings_names