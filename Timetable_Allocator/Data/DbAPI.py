import math
import sqlite3

from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


class DbAPI:
    '''API to interface with the DB'''

    def __init__(self):
        self.params = Parameters()
        self.db = sqlite3.connect(self.params.DB)

        # TODO: this DB is used to show the results in a comprehensive way using the GUI. In the final version it would be better to have only one DB with all the informations
        self.gui_db = sqlite3.connect("../../GUI_orario_Tesi/interface-server/Db_finale_postModifiche.db")

    '''
        Get all the teachings in the DB
        Return: list of teachings in format [ID_INC, nStudenti, nStudentiFreq, collegio, titolo, CFU, oreLez, titolare]
    '''
    def get_teachings(self):
        # TODO: getting only the mechatronic teachings, instead of the whole DB. The final query should be: SELECT * FROM Insegnamento
        cur = self.db.cursor()
        sql =   ("SELECT * FROM Insegnamento "
                 "WHERE id_inc IN "
                    "(SELECT id_inc FROM Insegnamento_in_Orientamento "
                        "WHERE nomeCdl='MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA)' "
                        "AND orientamento='Control Technologies for Industry 4.0')")
        cur.execute(sql)
        teachings = cur.fetchall()
        return teachings

    '''
        Get all the correlations info in the DB
        Return: list of correlations info in format [ID_INC_1, ID_INC_2, Correlazione, Correlazione_finale]
    '''
    def get_correlations_info(self):
        # TODO: getting only the correlations for mechatronic teachings, instead of the whole DB. The final query should be: SELECT * FROM Info_correlazioni
        cur = self.db.cursor()
        sql = ( "SELECT * FROM Info_correlazioni "
                "WHERE id_inc_1 IN "
                    "(SELECT id_inc FROM Insegnamento_in_Orientamento "
                        "WHERE nomeCdl='MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA)'"
                        "AND orientamento='Control Technologies for Industry 4.0')"
                "AND id_inc_2 IN "
                    "(SELECT id_inc FROM Insegnamento_in_Orientamento "
                    "WHERE nomeCdl='MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA)'"
                        "AND orientamento='Control Technologies for Industry 4.0')")
        cur.execute(sql)
        correlations = cur.fetchall()
        return correlations

    '''
        Saving the generated timetable to the GUI DB
    '''
    # TODO: in the final version of the project it would be better to have only one DB
    def save_results_to_db(self, solution, timetable_matrix, slots: list[int], teachings: list[Teaching]):
        cur = self.gui_db.cursor()

        # Deleting previous data from the DB
        sql = "DELETE FROM Slot WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)
        sql = "DELETE FROM PianoAllocazione WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)
        sql = "DELETE FROM Docente_in_Slot WHERE pianoAllocazione='Mechatronic_timetable'"
        cur.execute(sql)

        for s in slots:
            for t in teachings:
                if solution[timetable_matrix[t.id_teaching, s]] == 1:
                    # Assigning the slots to each Teaching
                    sql = ("INSERT INTO Slot (pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria, tipoLocale, tipoErogazione, capienzaAula, squadra, preseElettriche)"
                           "VALUES ('Mechatronic_timetable', '" + str(t.id_teaching) + "_slot_" + str(s) + "', -1, 'L', 1, " + t.id_teaching + ", '" + self.params.days[math.floor(s / self.params.slot_per_day)] + "', '" + self.params.time_slots[s % self.params.slot_per_day] + "', 'Aula', 'Presenza', 'NonDisponibile', 'No squadra', 'No')")
                    cur.execute(sql)

                    # Assigning the main Teacher of a Teaching to its Slot
                    sql = "INSERT INTO Docente_in_Slot (Cognome, idSlot, pianoAllocazione) VALUES ('" + t.main_teacher + "', '" + str(t.id_teaching) + "_slot_" + str(s) + "', 'Mechatronic_timetable')"
                    cur.execute(sql)

        # Inserting the new Allocation Plan
        sql = "INSERT INTO PianoAllocazione (pianoAllocazione) VALUES ('Mechatronic_timetable') "
        cur.execute(sql)

        self.gui_db.commit()

        print("\nResults saved in the DB")
