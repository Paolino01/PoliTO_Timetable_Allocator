import sqlite3
from Utils.Parameters import Parameters


class DbAPI:
    '''API to interface with the DB'''

    def __init__(self):
        params = Parameters()
        self.db = sqlite3.connect(params.DB)

    def get_teachings(self):
        '''
            Get all the teachings in the DB
            Return: list of teachings in format [ID_INC, nStudenti, nStudentiFreq, collegio, titolo, CFU, oreLez, titolare]
        '''
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

    def get_correlations_info(self):
        '''
            Get all the correlations info in the DB
            Return: list of correlations info in format [ID_INC_1, ID_INC_2, Correlazione, Correlazione_finale]
        '''
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