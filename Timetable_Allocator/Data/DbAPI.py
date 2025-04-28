import math
import sqlite3

from Utils.Components.Teacher import Teacher
from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


class DbAPI:
    '''API to interface with the DB'''

    def __init__(self):
        self.params = Parameters()
        self.db = sqlite3.connect(self.params.DB)

    '''Teachings'''

    '''
        Get all the first semester Teachings in the DB
        Return: list of teachings
    '''
    def get_teachings(self):
        cur = self.db.cursor()
        sql =   ("SELECT DISTINCT "
                    "Insegnamento.ID_INC, "
                    "titolo, "
                    "CFU, "
                    "titolare, "
                    "substring(periodoDidattico, 3, 1) AS periodoDidattico, "
                    "oreLez, "
                    "n_min_double_slots_lecture, "
                    "n_min_single_slots_lecture, "
                    "practice_hours, "
                    "n_practice_groups, "
                    "n_min_double_slots_practice, "
                    "n_min_single_slots_practice, "
                    "lab_hours, "
                    "n_lab_groups, "
                    "n_blocks_lab, "
                    "n_weekly_groups_lab, "
                    "double_slots_lab "
                 "FROM Insegnamento, Insegnamento_in_Orientamento "
                 "WHERE Insegnamento.ID_INC = Insegnamento_in_Orientamento.ID_INC "
                    "AND nomeCdl = ?")
        cur.execute(sql, ("INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)", ))
        teachings = cur.fetchall()
        return teachings

    '''
        Get all the correlations info in the DB
        Return: list of correlations info in format [ID_INC_1, ID_INC_2, Correlazione, Correlazione_finale]
    '''
    def get_correlations_info(self):
        cur = self.db.cursor()
        sql = "SELECT * FROM Info_correlazioni"
        cur.execute(sql)
        correlations = cur.fetchall()
        return correlations

    '''
        Get a previous solution that will be used as starting point to generate a new one
        Return: previous solution in format [allocationPlan, ID_INC, lectureType, day, timeSlot, lectGroup]
    '''
    def get_previous_solution(self):
        cur = self.db.cursor()
        sql = "SELECT * FROM PreviousSolution"
        cur.execute(sql)
        previous_solution = cur.fetchall()
        return previous_solution

    '''Teachers'''

    '''
        Get all the Teachers in the DB
        Return: list of Teachers in format [Surname]
    '''
    def get_teachers(self):
        cur = self.db.cursor()
        sql = "SELECT Cognome, ID_DOC FROM Docente"
        cur.execute(sql)
        teachers = cur.fetchall()
        return teachers

    '''
        Given a Teacher's ID, get all their Teachings
        Return: list of Teachings in format [ID_INC, tipoLez]
    '''
    def get_teachings_for_teacher(self, teacher_id):
        # I only consider courses where the Teacher has more than 7 hours, otherwise it would not be worth allocating a Slot
        cur = self.db.cursor()
        sql = "SELECT ID_INC, tipoLez FROM Docente_in_Insegnamento WHERE Cognome=? AND nOre > 7"
        cur.execute(sql, (teacher_id,))
        teachings_ids = cur.fetchall()
        return teachings_ids

    '''
        Given a Teacher, get all the Slots in which they are unavailable
        Return: list of Slots in format [Unavailable_Slot]
    '''
    def get_teachers_unavailabilities(self, teacher_id):
        cur = self.db.cursor()
        sql = "SELECT Unavailable_Slot FROM Teachers_Unavailability WHERE Teacher=?"
        cur.execute(sql, (teacher_id,))
        teachers_unavailabilities = cur.fetchall()
        return teachers_unavailabilities


    '''Timetable'''

    '''
        Saving the generated timetable in the DB
    '''
    def save_results_to_db(self, solution, timetable_matrix, slots: list[int], teachings: list[Teaching], teachers: list[Teacher]):
        cur = self.db.cursor()

        # Deleting previous data from the DB
        sql = "DELETE FROM Slot WHERE pianoAllocazione=?"
        cur.execute(sql, (self.params.timetable_name,))
        sql = "DELETE FROM PianoAllocazione WHERE pianoAllocazione=?"
        cur.execute(sql, (self.params.timetable_name,))
        sql = "DELETE FROM Docente_in_Slot WHERE pianoAllocazione=?"
        cur.execute(sql, (self.params.timetable_name,))

        for s in slots:
            for teaching in teachings:
                if solution[timetable_matrix[teaching.id_teaching, s]] == 1:
                    # Assigning the Slots to each Teaching
                    sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche) "
                           "VALUES (?, '" + str(teaching.id_teaching) + "_slot_" + str(s) + "', -1, 'L', 1, " + teaching.id_teaching + ", '" + self.params.days[math.floor(s / self.params.slot_per_day)] + "', '" + self.params.time_slots[s % self.params.slot_per_day] + "', 'Aula', 'Presenza', 'NonDisponibile', 'No squadra', 'No')")
                    cur.execute(sql, (self.params.timetable_name,))

                    # Assigning the Main Teacher to the Teaching's Slots
                    sql = "INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) VALUES (?, ?, ?)"
                    cur.execute(sql, (teaching.main_teacher_id, str(teaching.id_teaching) + "_slot_" + str(s), self.params.timetable_name))

                    # Assigning the collaborators of a Teaching to its Slots
                    for teacher in teachers:
                        if teacher.teacher_id != teaching.main_teacher_id:
                            for t in teacher.teachings:
                                # For each Teacher I check that the Teaching ID and Teaching Type matches.
                                # TODO: We can also add the Teachers related to a Teaching in the Teaching class, but we need to evaluate if it is better or not
                                if t[0].id_teaching == teaching.id_teaching and t[1] == "L":
                                    sql = "INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) VALUES (?, ?, ?)"
                                    cur.execute(sql, (teacher.teacher_id, str(teaching.id_teaching) + "_slot_" + str(s), self.params.timetable_name))

                '''Practice Slots'''
                self.save_practice_results_to_db(solution, timetable_matrix, teachers, teaching, s, cur)

                '''Lab Slots'''
                self.save_lab_results_to_db(solution, timetable_matrix, teachers, teaching, s, cur)


        # Inserting the new Allocation Plan
        sql = "INSERT INTO PianoAllocazione (pianoAllocazione) VALUES (?) "
        cur.execute(sql, (self.params.timetable_name,))

        self.db.commit()

        print("\nResults saved in the DB")

    def save_practice_results_to_db(self, solution, timetable_matrix, teachers, teaching, s, cur):
        # Adding Practice hours to the DB
        if teaching.practice_slots != 0:
            for i in range(1, teaching.n_practice_groups + 1):
                if solution[timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s]] == 1:
                    sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche) "
                           "VALUES (?, ?, -1, 'EA', 1, ?, ?, ?, 'Aula', 'Presenza', 'NonDisponibile', 'Squadra" + str(i) + "', 'No')")
                    cur.execute(
                        sql,
                        (
                            self.params.timetable_name,
                            str(teaching.id_teaching) + f"_practice_group{i}_slot_{s}",
                            teaching.id_teaching,
                            self.params.days[math.floor(s / self.params.slot_per_day)],
                            self.params.time_slots[s % self.params.slot_per_day]
                        )
                    )

                    # Assigning the collaborators of a Teaching to its Slots
                    # This variable is used to know if the Teaching has Collaborators. If not, we insert a temporary Teacher as collaborator
                    has_coll = False
                    for teacher in teachers:
                        for t in teacher.teachings:
                            # For each Teacher I check that the Teaching ID and Teaching Type matches.
                            # TODO: We can also add the Teachers related to a Teaching in the Teaching class, but we need to evaluate if it is better or not
                            if t[0].id_teaching == teaching.id_teaching and t[1] == "EA":
                                has_coll = True
                                sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                                       "VALUES (?,?, ?)")
                                cur.execute(
                                    sql,
                                    (
                                        teacher.teacher_id,
                                        str(teaching.id_teaching) + f"_practice_group{i}_slot_{s}",
                                        self.params.timetable_name
                                    )
                                )

                    if not has_coll:
                        sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                               "VALUES (?,?, ?)")
                        cur.execute(
                            sql,
                            (
                                teaching.id_teaching + "_practice_teacher",
                                str(teaching.id_teaching) + f"_practice_group{i}_slot_{s}",
                                self.params.timetable_name
                            )
                        )

    def save_lab_results_to_db(self, solution, timetable_matrix, teachers, teaching, s, cur):
        # Adding Lab hours to the DB
        if teaching.n_blocks_lab != 0:
            for i in range(1, teaching.n_lab_groups + 1):
                if solution[timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s]] == 1:
                    sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche)"
                           "VALUES (?, ?, -1, 'EL', 1, ?, ?, ?, 'Laboratorio', 'Presenza', 'NonDisponibile', 'Squadra" + str(i) + "', 'No')")
                    cur.execute(
                        sql,
                        (
                            self.params.timetable_name,
                            str(teaching.id_teaching) + f"_lab_group{i}_slot_{s}",
                            teaching.id_teaching,
                            self.params.days[math.floor(s / self.params.slot_per_day)],
                            self.params.time_slots[s % self.params.slot_per_day]
                        )
                    )

                    # Assigning the collaborators of a Teaching to its Slots
                    # This variable is used to know if the Teaching has Collaborators. If not, we insert a temporary Teacher as collaborator
                    has_coll = False
                    for teacher in teachers:
                        for t in teacher.teachings:
                            # For each Teacher I check that the Teaching ID and Teaching Type matches.
                            # TODO: We can also add the Teachers related to a Teaching in the Teaching class, but we need to evaluate if it is better or not
                            if t[0].id_teaching == teaching.id_teaching and t[1] == "EL":
                                has_coll = True

                                sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                                       "VALUES (?,?, ?)")
                                cur.execute(
                                    sql,
                                    (
                                        teacher.teacher_id,
                                        str(teaching.id_teaching) + f"_lab_group{i}_slot_{s}",
                                        self.params.timetable_name
                                    )
                                )

                    if not has_coll:
                        sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                               "VALUES (?,?, ?)")
                        cur.execute(
                            sql,
                            (
                                teaching.id_teaching + "_lab_teacher",
                                str(teaching.id_teaching) + f"_lab_group{i}_slot_{s}",
                                self.params.timetable_name
                            )
                        )