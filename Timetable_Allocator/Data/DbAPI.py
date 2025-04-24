import math
import sqlite3

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
                    "AND substring(periodoDidattico, 3, 1) = '1'")
        cur.execute(sql)
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
    def save_results_to_db(self, solution, timetable_matrix, slots: list[int], teachings: list[Teaching]):
        cur = self.db.cursor()

        # Deleting previous data from the DB
        sql = "DELETE FROM Slot WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)
        sql = "DELETE FROM PianoAllocazione WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)
        sql = "DELETE FROM Docente_in_Slot WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)

        for s in slots:
            for teaching in teachings:
                if solution[timetable_matrix[teaching.id_teaching, s]] == 1:
                    # Assigning the Slots to each Teaching
                    sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche) "
                           "VALUES ('Mechatronic_timetable', '" + str(teaching.id_teaching) + "_slot_" + str(s) + "', -1, 'L', 1, " + teaching.id_teaching + ", '" + self.params.days[math.floor(s / self.params.slot_per_day)] + "', '" + self.params.time_slots[s % self.params.slot_per_day] + "', 'Aula', 'Presenza', 'NonDisponibile', 'No squadra', 'No')")
                    cur.execute(sql)

                    # Assigning the main Teacher of a Teaching to its Slot
                    sql = "INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) VALUES (?, ?, 'Mechatronic_timetable')"
                    cur.execute(sql, (teaching.main_teacher_id, str(teaching.id_teaching) + "_slot_" + str(s)))

                # Adding Practice hours to the DB
                if teaching.practice_slots != 0:
                    for i in range(1, teaching.n_practice_groups + 1):
                        if solution[timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s]] == 1:
                            sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche) "
                                   "VALUES ('Mechatronic_timetable', ?, -1, 'EA', 1, ?, ?, ?, 'Aula', 'Presenza', 'NonDisponibile', 'Squadra" + str(i) + "', 'No')")
                            cur.execute(sql, (str(teaching.id_teaching) + f"_practice_group{i}_slot_{s}", teaching.id_teaching, self.params.days[math.floor(s / self.params.slot_per_day)], self.params.time_slots[s % self.params.slot_per_day]))

                            # Assigning the main Teacher of a Teaching to its Slot
                            # TODO: we should not have the main Teacher but the Practice Teacher(s)
                            sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                                   "VALUES (?,?, 'Mechatronic_timetable')")
                            cur.execute(sql, (teaching.main_teacher_id, str(teaching.id_teaching) + f"_practice_group{i}_slot_{s}"))

                # Adding Lab hours to the DB
                if teaching.n_blocks_lab != 0:
                    for i in range(1, teaching.n_lab_groups + 1):
                        if solution[timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s]] == 1:
                            sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche)"
                                    "VALUES ('Mechatronic_timetable', '" + str(teaching.id_teaching) + f"_lab_group{i}_slot_{s}" + "', -1, 'EL', 1, " + teaching.id_teaching + ", '" + self.params.days[math.floor(s / self.params.slot_per_day)] + "', '" + self.params.time_slots[s % self.params.slot_per_day] + "', 'Laboratorio', 'Presenza', 'NonDisponibile', 'Squadra" + str(i) + "', 'No')")
                            cur.execute(sql)

                            # Assigning the main Teacher of a Teaching to its Slot
                            # TODO: we should not have the main Teacher but the Lab Teacher(s)
                            sql = ("INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) "
                                   "VALUES (?, ?, 'Mechatronic_timetable')")
                            cur.execute(sql, (teaching.main_teacher_id, str(teaching.id_teaching) + f"_lab_group{i}_slot_{s}"))


        # Inserting the new Allocation Plan
        sql = "INSERT INTO PianoAllocazione (pianoAllocazione) VALUES ('Mechatronic_timetable') "
        cur.execute(sql)

        self.db.commit()

        print("\nResults saved in the DB")
