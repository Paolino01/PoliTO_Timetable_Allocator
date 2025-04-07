import math

from Data.DbAPI import DbAPI
from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


class Teachings:
    def __init__(self):
        self.teachings:list[Teaching] = []
        self.db_api = DbAPI()

        self.load_teachings_from_db()
        self.load_correlations_info_from_db()

    '''Load all the teachings from the db.'''
    def load_teachings_from_db(self):
        params = Parameters()

        list_teachings = self.db_api.get_teachings()

        for row in list_teachings:
            self.teachings.append(Teaching(
                id_teaching=str(row[0]),
                title=row[1],
                cfu=int(row[2]),
                main_teacher=row[3],
                didactic_period=row[4],

                lect_slots=math.ceil((int(row[5]) / params.n_weeks_in_semester) / params.hours_in_slot),
                n_min_double_slots_lecture=int(row[6]),
                n_min_single_slots_lecture=int(row[7]),

                practice_slots=math.ceil((int(row[8]) / params.n_weeks_in_semester) / params.hours_in_slot),
                n_practice_groups=int(row[9]),
                n_min_double_slots_practice=int(row[10]),
                n_min_single_slots_practice=int(row[11]),

                lab_slots=math.ceil((int(row[12]) / params.n_weeks_in_semester) / params.hours_in_slot),
                n_lab_groups=int(row[13]),
                n_blocks_lab=int(row[14]),
                n_weekly_groups_lab=int(row[15]),
                double_slots_lab=int(row[16])
            ))

    '''Load the correlations info from the db.'''
    def load_correlations_info_from_db(self):
        list_correlations = self.db_api.get_correlations_info()

        for row in list_correlations:
            # Get the item in self.teaching with the ID equal to ID_INC_1 and adds an element in the dictionary as [ID_INC_2] = correlation}
            teaching1 = next((t for t in self.teachings if t.id_teaching == str(row[0])), None)
            teaching2 = next((t for t in self.teachings if t.id_teaching == str(row[1])), None)

            if teaching1 is not None and teaching2 is not None:
                teaching1.set_correlations(teaching2, int(row[2]))

                # In the DB we only have teaching1, teaching2, corr and not teaching2, teaching1, corr. I add the second option to the Python structures
                teaching2.set_correlations(teaching1, int(row[2]))