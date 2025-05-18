import math

from Data.DbAPI import DbAPI
from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


'''
    Calculate the number of Slots per week per Lecture, Practice, and Lab
    Return the number of slots per week
'''
def calculate_slots_per_week(total_lecture_hours, total_practice_hours, total_lab_hours):
    params = Parameters()

    slots_fract_lecture = (total_lecture_hours / params.n_weeks_in_semester) / params.hours_in_slot
    slots_fract_practice = (total_practice_hours / params.n_weeks_in_semester) / params.hours_in_slot
    slots_fract_lab = (total_lab_hours / params.n_weeks_in_semester) / params.hours_in_slot

    # If I have, for example, 2.3 Slots per week I round them to 2. Otherwise, if I have 2.6 Slots per week, I round them to 3
    # This can be done in a shorter way, but I kept it like this for better clarity
    slots_lecture = math.floor(slots_fract_lecture) \
        if slots_fract_lecture - math.floor(slots_fract_lecture) <= 0.35 \
        else math.ceil(slots_fract_lecture)

    slots_practice = math.floor(slots_fract_practice) \
        if slots_fract_practice - math.floor(slots_fract_practice) <= 0.35 \
        else math.ceil(slots_fract_practice)

    slots_lab = math.floor(slots_fract_lab) \
        if slots_fract_lab - math.floor(slots_fract_lab) <= 0.35 \
        else math.ceil(slots_fract_lab)

    return slots_lecture, slots_practice, slots_lab

class Teachings:
    def __init__(self):
        self.teachings_list:list[Teaching] = []
        self.db_api = DbAPI()


    '''Load all the teachings from the db.'''
    def load_teachings_from_db(self, courses):
        list_teachings = self.db_api.get_teachings(courses)

        for row in list_teachings:
            # Calculate the number of Slots in a week for Lectures, Practices and Labs
            slots_lecture, slots_practice, slots_lab = calculate_slots_per_week(int(row[5]), int(row[8]), int(row[12]))

            if slots_practice > 0:
                n_practice_groups = int(row[9])
                n_min_double_slots_practice = int(row[10])
                n_min_single_slots_practice = int(row[11])
            else:
                n_practice_groups = 0
                n_min_double_slots_practice = 0
                n_min_single_slots_practice = 0

            if slots_lab > 0:
                n_lab_groups = int(row[13])
                n_blocks_lab = int(row[14])
                n_weekly_groups_lab = int(row[15])
                double_slots_lab = int(row[16])
            else:
                n_lab_groups = 0
                n_blocks_lab = 0
                n_weekly_groups_lab = 0
                double_slots_lab = 0

            if slots_lecture > 0:
                self.teachings_list.append(Teaching(
                    id_teaching=str(row[0]),
                    title=row[1],
                    cfu=int(row[2]),
                    main_teacher_id=row[3],
                    didactic_period=row[4],

                    lect_slots=slots_lecture,
                    n_min_double_slots_lecture=int(row[6]),
                    n_min_single_slots_lecture=int(row[7]),

                    practice_slots=slots_practice,
                    n_practice_groups=n_practice_groups,
                    n_min_double_slots_practice=n_min_double_slots_practice,
                    n_min_single_slots_practice=n_min_single_slots_practice,

                    lab_slots=slots_lab,
                    n_lab_groups=n_lab_groups,
                    n_blocks_lab=n_blocks_lab,
                    n_weekly_groups_lab=n_weekly_groups_lab,
                    double_slots_lab=double_slots_lab
                ))

        self.load_correlations_info_from_db()

    '''Load the correlations info from the db.'''
    def load_correlations_info_from_db(self):
        list_correlations = self.db_api.get_correlations_info()

        for row in list_correlations:
            # Get the item in self.teaching with the ID equal to ID_INC_1 and adds an element in the dictionary as [ID_INC_2] = correlation
            teaching1 = next((t for t in self.teachings_list if t.id_teaching == str(row[0])), None)
            teaching2 = next((t for t in self.teachings_list if t.id_teaching == str(row[1])), None)

            if teaching1 is not None and teaching2 is not None:
                teaching1.set_correlations(teaching2, int(row[2]))

                # In the DB we only have teaching1, teaching2, corr and not teaching2, teaching1, corr. I add the second option to the Python structures
                teaching2.set_correlations(teaching1, int(row[2]))