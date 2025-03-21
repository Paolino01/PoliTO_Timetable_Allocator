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

    # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
    timetable_matrix = {(t.id_teaching, s): model.binary_var(name=f"x_{t.id_teaching}_{s}") for t in teachings for s in slots}

    # Constraint: each Teaching must have exactly cfu/2 Slots per week
    for t in teachings:
        model.add_constraint(model.sum(timetable_matrix[t.id_teaching, s] for s in slots) == math.floor(t.cfu/2))

    for s in slots:
        for t1 in teachings:
            # Constraint: limiting the number of correlated lectures in a day. For example, I impose that the sum of the correlations between lectures in a day should be <= params.max_corr_in_day
            # This way I don't limit the number of consecutive lecture slots
            model.add_constraint(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s + i])
                for i in range(1, params.slot_per_day - (s % params.slot_per_day))
                for t2_id, corr in t1.correlations.items()) <= params.max_corr_in_day)

            # Constraint: a Teaching cannot overlap with the others, according to the correlations
            for t2_id, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from 267072 to 267158 and the other from 267158 to 267072)
                if t1.id_teaching < t2_id:
                    model.add_constraint(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s] <= 1)

    # Constraint: I consider 3 consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
    # TODO: needs testing
    for s in range(len(slots) - 2):
        for t1 in teachings:
            correlations_in_slots = model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s + i])
                for i in range(1, 3)
                for t2_id, corr in t1.correlations.items())

            model.add(1 == model.logical_or(correlations_in_slots <= 0, correlations_in_slots >= params.min_corr_in_slots))

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
                print(f"{t.id_teaching}: {[int(solution[timetable_matrix[t.id_teaching, s]]) for s in slots]}")
    else:
        print("\nNo solution found.")