import math

from docplex.cp.model import CpoModel
from Components.Slots import get_slots_per_week
from Utils.Hooks.Teachings import Teachings
from Utils.Parameters import Parameters

'''
    This function returns the correlation value between two teachings that are in the same day in different slots
'''
def get_corr_value():
    if timetable_matrix[t, s] == 1:
        return
    else:
        return 0

if __name__ == '__main__':
    # Problem definition
    model = CpoModel(name="PoliTO_Timetable_Scheduling")

    params = Parameters()

    # List of Teachings that I need to allocate
    teachings_class = Teachings()
    teachings = teachings_class.teachings

    # Number of slots per week
    slots = get_slots_per_week()
    # Number of days per week
    days = range(0, (6 if params.saturday_enabled else 5))

    # Weight of the Teachings in a day
    day_load = [0] * (6 if params.saturday_enabled else 5)

    # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
    timetable_matrix = {(t.id_teaching, s): model.binary_var(name=f"x_{t.id_teaching}_{s}") for t in teachings for s in slots}

    # Constraint: each Teaching must have exactly cfu/2 Slots per week
    for t in teachings:
        model.add_constraint(model.sum(timetable_matrix[t.id_teaching, s] for s in slots) == math.floor(t.cfu/2))

    # Constraint: a Teaching cannot overlap with the others, according to the correlations
    for s in slots:
        for t1 in teachings:
            for t2_id, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from 267072 to 267158 and the other from 267158 to 267072)
                if t1.id_teaching < t2_id:
                    model.add_constraint(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s] <= 1)

                # Constraint: limiting the number of "correlated lectures" in a day. For example, I impose that the sum of the correlations between lectures in a day should be < 400
                # This way I don't limit the number of consecutive lecture slots
                # TODO: needs to be tested
                model.add_constraint(model.sum(corr * (timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s + i]) for i in range(0, params.slot_per_day - (s % params.slot_per_day))) <= params.max_corr_in_day)

    # Another idea:
    # Constraint: limiting the number of "correlated lectures" in a day. For example, I impose that the sum of the correlations between lectures in a day should be < 400
    # This way I don't limit the number of consecutive lecture slots
    '''
    for d in days:
        dayly_load = 0
        teachings_in_day = [t for t in teachings if (timetable_matrix[t.id_teaching, s] for s in slots if math.floor(s/params.slot_per_day) == d)]
        for t in teachings_in_day:
            print (t.id_teaching)
        print("----")
    '''

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
                print(f"{t.id_teaching}: {[int(solution[timetable_matrix[t.id_teaching, s]]) for s in slots]}")
    else:
        print("No solution found.")