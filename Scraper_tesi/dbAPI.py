# from calendar import c
# import sqlite3
# from typing import List, Tuple

# from patterns import *



# class dbAPI(metaclass=SingletonMeta):
#     '''API per interfacciarsi col db.
#     Syntax: actions_object'''
#     def __init__(self, dbPath):
#         self.DB = dbPath
#         self.db = sqlite3.connect(self.DB)    

#     def get_Orientamenti(self):
#         '''Return: 
#             [orientamento, nomeCdl, tipoCdl]'''
#         cur = self.db.cursor()
#         cur.execute("SELECT * FROM Orientamento")
#         return cur.fetchall()
    
#     # Aggiunto Manuel
#     def get_ID_INC_from_codIns(self, codIns:str):
#         '''Return:
#             [ID_INC]'''
#         cur = self.db.cursor()
#         sql = '''SELECT ID_INC
#                 FROM Insegnamento_listCodIns
#                 WHERE codIns = ?'''
#         cur.execute(sql, (codIns,))
#         return cur.fetchall()
    
    
#     def insert_info_correlazione(self, id1, id2, correlazione):
#         if(all(x != int for x in [type(id1),type(id2), type(correlazione)])):
#             print('ERRORE VALORI PASSATI')
#             return None
#         '''
#             Inserisce per una coppia di ID_INC il valore di correlazione'''
#         cur = self.db.cursor()
#         sql = '''INSERT INTO Info_correlazioni VALUES(?,?,?,NULL)'''
#         cur.execute(sql, (id1,id2,correlazione))
#         self.db.commit()
    
#     def clear_info_correlazioni(self):
#         '''
#             Cancella i valori nella tabella Info_correlazioni'''
#         cur = self.db.cursor()
#         sql = '''DELETE FROM Info_correlazioni'''
#         cur.execute(sql)
#         self.db.commit()

#     def get_correlazione_coppia(self, id1, id2):
#         '''
#             Restituisce il valore di correlazione di una coppia di ID_INC'''
#         cur = self.db.cursor()
#         sql = '''SELECT Correlazione
#                 FROM Info_correlazioni
#                 WHERE (ID_INC_1 = ? and ID_INC_2 = ?) or (ID_INC_1 = ? and ID_INC_2 = ?)'''
#         cur.execute(sql, (id1,id2,id2,id1))
#         return cur.fetchone()
    
#     def get_titolare(self, id_inc):
#         cur = self.db.cursor()
#         sql = '''SELECT titolare
#                 FROM Insegnamento
#                 WHERE ID_INC = ?'''
#         cur.execute(sql, (id_inc,))
#         return cur.fetchone()
    
#     def update_InsegnamentiInOrientamento(self, orientamento:str, nomeCdl:str, tipoCdl:str, periodoDidattico:str, tipoInsegnamento:str, id_inc):
#         '''Aggiorna in Insegnamento_in_Orientamento tutti gli Insegnamenti passati nella lista come Insegnamenti per l'Orientamento e il cdl 
#         correnti; con il relativo grado di importanza (TipoInsegnamento) e il periodo didattico.'''
#         cur = self.db.cursor()
#         sql = '''UPDATE Insegnamento_in_Orientamento
#                 SET tipoInsegnamento = ?, periodoDidattico = ?
#                 WHERE ID_INC = ? AND orientamento = ? AND nomeCdl = ? AND tipoCdl = ?'''
#         try:
#             cur.execute(sql, (tipoInsegnamento, periodoDidattico, id_inc, orientamento, nomeCdl, tipoCdl))
#         except Exception as e:
#             print("ERR dbAPI.update_InsegnamentiInOrientamento(): " + str(e))
#             print("ERR for data: " + str(id_inc) + ", " + str(orientamento) + ", " + str(nomeCdl) + ", " + str(tipoCdl))
#         self.db.commit() 
#     # Fine Aggiunto Manuel
    
#     def get_Alfabetiche_ofInsegnamento(self, ID_INC:int):
#         '''Ritorna le alfabetiche di un Insegnamento (possono essere più di una):
#         Return:
#             [alfabetica]'''
#         sql = '''SELECT alfabetica
#                 FROM Insegnamento_in_Orientamento
#                 WHERE ID_INC = ?'''
#         cur = self.db.cursor()
#         cur.execute(sql, (ID_INC,))
#         return cur.fetchall()
    
#     def get_CodInsInsegnamento(self, ID_INC:str):
#         '''Return: 
#             [codIns]
#         '''
#         cur = self.db.cursor()
#         sql = '''SELECT codIns
#                 FROM Insegnamento_listCodIns
#                 WHERE ID_INC = ?'''
#         cur.execute(sql, [ID_INC])
#         return cur.fetchall()
    
#     def commit(self):
#         self.db.commit()
        
#     def rollback(self):
#         self.db.rollback()


# Import required libraries
from calendar import c
import sqlite3
from typing import List, Tuple

from patterns import *

# Database API class (Singleton Pattern)
class dbAPI(metaclass=SingletonMeta):
    '''API to interact with the SQLite database.
    
    Syntax: actions_object
    '''
    
    def init(self, dbPath):
        '''Initializes the database connection.

        Args:
            dbPath (str): The file path of the SQLite database.
        '''
        self.DB = dbPath
        self.db = sqlite3.connect(self.DB)

    def get_Orientamenti(self):
        '''Fetch all orientations from the database.
        
        Returns:
            List of tuples containing [orientation, degree name (nomeCdl), degree type (tipoCdl)]
        '''
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Orientamento")
        return cur.fetchall()
    
    # Added by Manuel
    def get_ID_INC_from_codIns(self, codIns: str):
        '''Retrieve the ID_INC (unique ID) for a given course code.

        Args:
            codIns (str): Course code.
        
        Returns:
            List containing [ID_INC]
        '''
        cur = self.db.cursor()
        sql = '''SELECT ID_INC
                FROM Insegnamento_listCodIns
                WHERE codIns = ?'''
        cur.execute(sql, (codIns,))
        return cur.fetchall()
    
    def insert_info_correlazione(self, id1, id2, correlazione):
        '''Insert correlation information between two courses based on their ID_INC.

        Args:
            id1 (int): First course ID.
            id2 (int): Second course ID.
            correlazione (int): Correlation value between the courses.

        Returns:
            None (but inserts data into the database)
        '''
        # Ensure that all input values are integers
        if all(x != int for x in [type(id1), type(id2), type(correlazione)]):
            print('ERROR: Invalid values passed')
            return None
        
        cur = self.db.cursor()
        sql = '''INSERT INTO Info_correlazioni VALUES(?,?,?,NULL)'''
        cur.execute(sql, (id1, id2, correlazione))
        self.db.commit()
    
    def clear_info_correlazioni(self):
        '''Deletes all values in the Info_correlazioni table.'''
        cur = self.db.cursor()
        sql = '''DELETE FROM Info_correlazioni'''
        cur.execute(sql)
        self.db.commit()

    def get_correlazione_coppia(self, id1, id2):
        '''Retrieve the correlation value between two courses based on their IDs.

        Args:
            id1 (int): First course ID.
            id2 (int): Second course ID.
        
        Returns:
            Tuple containing (correlation value) or None if not found.
        '''
        cur = self.db.cursor()
        sql = '''SELECT Correlazione
                FROM Info_correlazioni
                WHERE (ID_INC_1 = ? and ID_INC_2 = ?) or (ID_INC_1 = ? and ID_INC_2 = ?)'''
        cur.execute(sql, (id1, id2, id2, id1))
        return cur.fetchone()
    
    def get_titolare(self, id_inc):
        '''Retrieve the course instructor (titolare) for a given course ID.

        Args:
            id_inc (int): Course ID.
        
        Returns:
            Tuple containing (course instructor name).
        '''
        cur = self.db.cursor()
        sql = '''SELECT titolare
                FROM Insegnamento
                WHERE ID_INC = ?'''
        cur.execute(sql, (id_inc,))
        return cur.fetchone()
    
    def update_InsegnamentiInOrientamento(self, orientamento: str, nomeCdl: str, tipoCdl: str, periodoDidattico: str, tipoInsegnamento: str, id_inc):
        '''Update an entry in the Insegnamento_in_Orientamento table with new teaching period and importance level.

        Args:
            orientamento (str): Orientation name.
            nomeCdl (str): Course degree name.
            tipoCdl (str): Type of degree.
            periodoDidattico (str): Teaching period.
            tipoInsegnamento (str): Importance level of the course.
            id_inc (int): Course ID.
        
        Returns:
        
        None (updates the database)
        
        '''
        cur = self.db.cursor()
        sql = '''UPDATE Insegnamento_in_Orientamento
                SET tipoInsegnamento = ?, periodoDidattico = ?
                WHERE ID_INC = ? AND orientamento = ? AND nomeCdl = ? AND tipoCdl = ?'''
        try:
            cur.execute(sql, (tipoInsegnamento, periodoDidattico, id_inc, orientamento, nomeCdl, tipoCdl))
        except Exception as e:
            print("ERROR in dbAPI.update_InsegnamentiInOrientamento(): " + str(e))
            print("ERROR for data: " + str(id_inc) + ", " + str(orientamento) + ", " + str(nomeCdl) + ", " + str(tipoCdl))
        self.db.commit()
    
    # End of Manuel's added methods

    def get_Alfabetiche_ofInsegnamento(self, ID_INC: int):
        '''Retrieve the alphabetical categories of a course (multiple possible).

        Args:
            ID_INC (int): Course ID.
        
        Returns:
            List containing [alphabetical category].
        '''
        sql = '''SELECT alfabetica
                FROM Insegnamento_in_Orientamento
                WHERE ID_INC = ?'''
        cur = self.db.cursor()
        cur.execute(sql, (ID_INC,))
        return cur.fetchall()
    
    def get_CodInsInsegnamento(self, ID_INC: str):
        '''Retrieve the course code for a given course ID.

        Args:
            ID_INC (str): Course ID.
        
        Returns:
            List containing [codIns] (course codes).
        '''
        cur = self.db.cursor()
        sql = '''SELECT codIns
                FROM Insegnamento_listCodIns
                WHERE ID_INC = ?'''
        cur.execute(sql, [ID_INC])
        return cur.fetchall()
    
    def commit(self):
        '''Commit the current transaction.'''
        self.db.commit()
        
    def rollback(self):
        '''Rollback the last transaction.'''
        self.db.rollback()