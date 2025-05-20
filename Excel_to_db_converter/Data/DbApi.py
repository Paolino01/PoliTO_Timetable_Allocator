import sqlite3

class DbApi:
    def __init__(self):
        self.db = sqlite3.connect("../Data/Courses_DB.db")

    '''
        Delete all the Teachings from the DB, in order to be ready to insert new ones
    '''
    def delete_all_teachings(self):
        cur = self.db.cursor()

        sql = "DELETE FROM Corso_di_laurea"
        cur.execute(sql)

        sql = "DELETE FROM Orientamento"
        cur.execute(sql)

        sql = "DELETE FROM Insegnamento_listCodIns"
        cur.execute(sql)

        sql = "DELETE FROM Insegnamento"
        cur.execute(sql)

        sql = "DELETE FROM Insegnamento_in_Orientamento"
        cur.execute(sql)

        self.db.commit()

    '''
        Insert a Degree Course with its type in DB, if not present.
        Then, add the orientations to that Degree.
        Finally, add the Teaching to the Orientation
    '''
    def insert_teachings(self, course_type, course_name, orientation, ID_INC, id_teaching, college, teaching_name, cfu, main_teacher, teaching_type, didactic_period, alphabetic_number):
        cur = self.db.cursor()

        sql = "INSERT OR IGNORE INTO Corso_di_laurea(tipoCdl, nomeCdl) VALUES (?, ?)"
        cur.execute(sql, (course_type, course_name))

        sql = "INSERT OR IGNORE INTO Orientamento(orientamento, nomeCdl, tipoCdl) VALUES (?, ?, ?)"
        cur.execute(sql, (orientation, course_name, course_type))

        sql = "INSERT OR IGNORE INTO Insegnamento_listCodIns(ID_INC, codIns) VALUES (?, ?)"
        cur.execute(sql, (ID_INC, id_teaching))

        sql = "INSERT OR IGNORE INTO Insegnamento(ID_INC, collegio, titolo, CFU, titolare, oreLez) VALUES (?, ?, ?, ?, ?, 0)"
        cur.execute(sql, (ID_INC, college, teaching_name, cfu, main_teacher))

        sql = "INSERT OR IGNORE INTO Insegnamento_in_Orientamento(ID_INC, orientamento, nomeCdl, tipoInsegnamento, tipoCdl, periodoDidattico, alfabetica) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sql, (ID_INC, orientation, course_name, teaching_type, course_type, didactic_period, alphabetic_number))

        self.db.commit()

    '''
        Get all the teachings in the DB
        Return: list of teachings in format [ID_INC, titolo, titolare]
    '''
    def get_teachings(self):
        cur = self.db.cursor()
        sql = "SELECT ID_INC, titolo, titolare FROM Insegnamento"
        cur.execute(sql)
        teachings = cur.fetchall()
        return teachings

    '''
        Get all the Oientations in the DB
        Returns: list of Oientations in format [orientamento, nomeCdl, tipoCdl]
    '''
    def get_orientations(self):
        cur = self.db.cursor()
        sql = "SELECT * FROM Orientamento"
        cur.execute(sql)
        orientations = cur.fetchall()
        return orientations

    '''
        Get all the Teachings in an Orientation
        Returns: list of Teachings in format [ID_INC, tipoInsegnamento, periodoDidattico, alfabetica]
    '''
    def get_teachings_in_orientation(self, orientation):
        cur = self.db.cursor()
        sql = "SELECT ID_INC, tipoInsegnamento, periodoDidattico, alfabetica FROM Insegnamento_in_Orientamento WHERE orientamento = ? AND nomeCdl = ? AND tipoCdl = ?"
        cur.execute(sql, (orientation[0], orientation[1], orientation[2]))
        teachings = cur.fetchall()
        return teachings

    '''
        Remove the Correlation Info from the DB
    '''
    def remove_correlation_info(self):
        cur = self.db.cursor()
        sql = "DELETE FROM Info_correlazioni"
        cur.execute(sql)
        self.db.commit()

    '''
        Insert the correlation between two Teachings in the DB
    '''
    def insert_correlation(self, ID_INC_1, ID_INC_2, correlation, mandatory):
        cur = self.db.cursor()

        sql = "SELECT Correlazione FROM Info_correlazioni WHERE ID_INC_1=? AND ID_INC_2=?"
        cur.execute(sql, (ID_INC_1, ID_INC_2))
        corr = cur.fetchone()

        if corr is None:
            sql = "INSERT INTO Info_correlazioni (ID_INC_1, ID_INC_2, Correlazione, Obbligatorio) VALUES (?, ?, ?, ?)"
            cur.execute(sql, (ID_INC_1, ID_INC_2, correlation, mandatory))
        else:
            if corr[0] < correlation:
                sql = "UPDATE Info_correlazioni SET Correlazione = ? WHERE ID_INC_1=? AND ID_INC_2=?"
                cur.execute(sql, (correlation, ID_INC_1, ID_INC_2))

        self.db.commit()

    '''
        Delete all records from Docente_in_Insegnamento
    '''
    def delete_teacher_in_teaching(self):
        cur = self.db.cursor()
        sql = "DELETE FROM Docente_in_Insegnamento"
        cur.execute(sql)

        self.db.commit()

    '''
        Update a Teaching in the DB with the hours of lectures and the name of the main teacher
    '''
    def add_teacher_and_lecture_hours_to_course(self, id_inc, lecture_hours, main_teacher_id):
        cur = self.db.cursor()
        sql = "UPDATE Insegnamento SET oreLez = ?, titolare = ? WHERE ID_INC = ?"
        cur.execute(sql, (lecture_hours, main_teacher_id, id_inc))

        sql = "INSERT INTO Docente_in_Insegnamento (Cognome, ID_INC, nOre, tipoLez) VALUES (?, ?, 0, 'L')"
        cur.execute(sql, (main_teacher_id, id_inc))

        self.db.commit()

    '''
        Update the Teacher of a Teaching and add their hours
    '''
    def add_teacher_hours(self, teacher_id, hours, lecture_type, teaching_id):
        cur = self.db.cursor()
        sql = "UPDATE Docente_in_Insegnamento SET nOre = ? WHERE Cognome = ? AND ID_INC = ? AND TipoLez = ?"
        cur.execute(sql, (hours, teacher_id, teaching_id, lecture_type))
        self.db.commit()

    '''
        Insert a Teacher in a Teaching with its hours
    '''
    def add_teacher_in_teaching(self, teacher_id, hours, lecture_type, teaching_id):
        # Note: we have to retrieve the full name of the Teacher starting from teacher_surname
        cur = self.db.cursor()
        sql = "SELECT * FROM Docente_in_Insegnamento WHERE Cognome = ? AND ID_INC = ? AND tipoLez = ?"
        cur.execute(sql, (teacher_id, teaching_id, lecture_type))

        if len(cur.fetchall()) == 0:
            sql = "INSERT INTO Docente_in_Insegnamento (Cognome, ID_INC, nOre, tipoLez) VALUES (?, ?, ?, ?)"
            cur.execute(sql, (teacher_id, teaching_id, hours, lecture_type))
            self.db.commit()
        else:
            self.add_teacher_hours(teacher_id, hours, lecture_type, teaching_id)

    '''
        Update a Teaching in the DB with the info about organizations of lecture, practice, and lab hours
    '''
    def insert_teaching_preference(
            self,
            title,
            main_teacher_id,
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
            double_slots_lab,
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
               "double_slots_lab = ?"
               "WHERE lower(titolo) = ? AND titolare = ?")

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
            double_slots_lab,
            title.lower(),
            main_teacher_id,
        ))

        self.db.commit()

    '''
        Delete all the Teachers_Unavailability entries    
    '''
    def clear_teachers_unavailabilities(self):
        cur = self.db.cursor()
        sql = "DELETE FROM Teachers_Unavailability"
        cur.execute(sql)
        self.db.commit()

    '''
        Given a Teacher's name, get their ID
    '''
    def get_teacher_id(self, teacher):
        cur = self.db.cursor()
        sql = "SELECT ID_DOC FROM Docente WHERE Cognome = ?"
        cur.execute(sql, (teacher,))
        teacher_id = cur.fetchall()
        return teacher_id

    '''
        Insert an unavailable Slot for a Teacher
    '''
    def insert_unavailable_slot(self, teacher_id, slot):
        cur = self.db.cursor()

        # Check that the couple Teacher, Unavailable_Slot does not already exists in the database
        sql = "SELECT count(*) FROM Teachers_Unavailability WHERE Teacher = ? AND Unavailable_Slot = ?"
        cur.execute(sql, (teacher_id, slot))

        if cur.fetchone()[0] == 0:
            sql = "INSERT INTO Teachers_Unavailability VALUES (?, ?)"
            cur.execute(sql, (teacher_id, slot))
            self.db.commit()