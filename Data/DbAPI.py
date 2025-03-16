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
        cur = self.db.cursor()
        sql = "SELECT * FROM Insegnamento"
        cur.execute(sql)
        teachings = cur.fetchall()
        return teachings

    def get_correlations_info(self):
        '''
        Get all the correlations info in the DB
        Return: list of correlations info in format [ID_INC_1, ID_INC_2, Correlazione, Correlazione_finale]
        '''
        cur = self.db.cursor()
        sql = "SELECT * FROM Info_correlazioni"
        cur.execute(sql)
        correlations = cur.fetchall()
        return correlations