from Data.DbAPI import DbAPI
from Utils.Interfaces.Teaching import Teaching

class Teachings:
    def __init__(self):
        self.teachings:list[Teaching] = []
        self.db_api = DbAPI()

        self.load_teachings_from_db()
        self.load_correlations_info_from_db()

    '''Load all the teachings from the db.'''
    def load_teachings_from_db(self):
        list_teachings = self.db_api.get_teachings()

        for row in list_teachings:
            self.teachings.append(Teaching(str(row[0]), int(row[1]), int(row[2]), row[3], row[4], int(row[5]), int(row[6]), row[7]))

    '''Load the correlations info from the db.'''
    def load_correlations_info_from_db(self):
        list_correlations = self.db_api.get_correlations_info()

        for row in list_correlations:
            # Get the item in self.teaching with the ID equal to ID_INC_1 and adds an element in the dictionary as [ID_INC_2] = correlation}
            teaching = next((t for t in self.teachings if t.id_teaching == str(row[0])), None)

            if teaching is not None:
                teaching.set_correlations(str(row[1]), int(row[2]))

            # Adding a correlation of 100 with the same teaching
            teaching.set_correlations(str(row[0]), 100)
