import math

from docplex.cp.model import CpoModel
from docplex.cp.modeler import logical_or

from Components.Slots import get_slots_per_week
from Data.DbAPI import DbAPI
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
    db_api = DbAPI()

    # List of Teachings that I need to allocate
    teachings_class = Teachings()
    teachings = teachings_class.teachings

    # Number of slots per week
    slots = get_slots_per_week()
    # Number of days per week
    days = range(5 if params.saturday_enabled == False else 6)

    # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
    timetable_matrix = {(t.id_teaching, s): model.binary_var(name=f"x_{t.id_teaching}_{s}") for t in teachings for s in slots}

    #Variable that counts how many hours a teaching has in a day
    n_slots_in_day_teaching = {(t.id_teaching, d): model.integer_var(0, 2, name=f"y_{t.id_teaching}_{d}") for t in teachings for d in days}
    # Variable that is 1 if the Teaching t appears in Day d, 0 otherwise
    n_days_teaching = {(t.id_teaching, d): model.binary_var(name=f"y_{t.id_teaching}_{d}") for t in teachings for d in days}

    # Constraint: each Teaching must have exactly cfu/2 Slots per week
    for t in teachings:
        model.add_constraint(model.sum(timetable_matrix[t.id_teaching, s] for s in slots) == math.floor(t.cfu/2))

    # Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
    # Constraint: each Teaching must appear in a maximum of params.max_days_teaching days
    # TODO: this constraint should only be applied to Lecture Slots and not Laboratory Slots
    # TODO: maybe I can add a parameter for the maximum number of consecutive Slots
    # TODO: the maximum number of days is modeled as an hard constraint for testing purposes, but may be better as a soft constraint (not done for now 'cause I'm not considering soft constraints yet)
    for t in teachings:
        for d in days:
            # Counts how many hours the Teaching t has in Day d
            model.add(n_slots_in_day_teaching[t.id_teaching, d] == model.sum(timetable_matrix[t.id_teaching, s] for s in range(d * params.slot_per_day, (d+1) * params.slot_per_day)))
            # Counts in how many days the Teaching t appears
            model.add(n_days_teaching[t.id_teaching, d] >= n_slots_in_day_teaching[t.id_teaching, d] / 2)
            model.add(n_days_teaching[t.id_teaching, d] <= n_slots_in_day_teaching[t.id_teaching, d])

            # Add the constraint that a Teaching should have a maximum of 2 Slots in a day (only for Lectures and not for Laboratories)
            model.add(n_slots_in_day_teaching[t.id_teaching, d] <= 2)
            # Add the constraint that a Teaching must appear in a maximum of params.max_days_teaching
            model.add(model.sum(n_days_teaching[t.id_teaching, day] for day in days) <= params.max_days_teaching)

            # If n_slots_in_day_teaching[t.id_teaching, d] == 2, the two Slots should be consecutive
            for s in range(len(slots) - 1):
                if math.floor(s / params.slot_per_day) == d and math.floor((s+1) / params.slot_per_day) == d:
                    model.add(model.logical_or(timetable_matrix[t.id_teaching, s] == 0, (timetable_matrix[t.id_teaching, s] + timetable_matrix[t.id_teaching, s+1]) >= n_slots_in_day_teaching[t.id_teaching, d]))

    for s in slots:
        for t1 in teachings:
            # Constraint: limiting the number of correlated lectures in a day. For example, I impose that the sum of the correlations between lectures in a day should be <= params.max_corr_in_day
            # This way I don't limit the number of consecutive lecture slots
            model.add_constraint(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s + i])
                for i in range(1, params.slot_per_day - (s % params.slot_per_day)) if s+i in slots
                for t2_id, corr in t1.correlations.items()) <= params.max_corr_in_day)

            # Constraint: a Teaching cannot overlap with the others, according to the correlations
            for t2_id, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from 267072 to 267158 and the other from 267158 to 267072)
                if t1.id_teaching < t2_id:
                    model.add_constraint(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s] <= 1)

    # Constraint: I consider 3 consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
    for s in range(len(slots) - 2):
        for t1 in teachings:
            correlations_in_slots = model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2_id, s + i])
                for i in range(1, 3)
                for t2_id, corr in t1.correlations.items())

            model.add(1 == model.logical_or(correlations_in_slots == 0, correlations_in_slots >= params.min_corr_in_slots))

    # Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
    for t1 in teachings:
        for t2_id, corr in t1.correlations.items():
            model.add(model.sum(corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2_id, s + (params.slot_per_day-1)]) for s in range(0, 35, 7)) <= params.max_corr_first_last_slot)

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
            print(f"{t.id_teaching}: {[int(solution[timetable_matrix[t.id_teaching, s]]) for s in slots]}")

        # Saving the results to the DB
        db_api.save_results_to_db(solution, timetable_matrix, slots, teachings)
    else:
        print("\nNo solution found.")