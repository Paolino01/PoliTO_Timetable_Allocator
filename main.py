import math

from docplex.cp.model import CpoModel
from Components.Slots import get_slots_per_week
from Utils.Hooks.Teachings import Teachings
from Utils.Parameters import Parameters

if __name__ == '__main__':
    # Problem definition
    model = CpoModel(name="PoliTO_Timetable_Scheduling")

    params = Parameters()

    # List of Teachings that I need to allocate
    teachings_class = Teachings()
    teachings = teachings_class.teachings

    # TODO: limiting the number of teachings so that I stay under the 1000 vars included in the trial version of CPLEX
    teachings = teachings[:25]

    # Number of slots per week
    slots = get_slots_per_week()

    # Binary variables x[s,t] = 1 if the Teaching 't' is assigned to Slot 's'
    x = {(t.id_teaching, s): model.binary_var(name=f"x_{t.id_teaching}_{s}") for t in teachings for s in slots}

    # Constraint: each Teaching must have exactly cfu/2 Slots per week
    for t in teachings:
        model.add_constraint(model.sum(x[t.id_teaching, s] for s in slots) == math.floor(t.cfu/2))

    # Constraint: a Teaching cannot overlap with the others, according to the correlations
    for s in slots:
        for t1 in teachings:
            for t_id, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from 267072 to 267158 and the other from 267158 to 267072)
                if t1.id_teaching < t_id:
                    # TODO: the following if is needed in order to run the program with a limited number of teachings (see line 15)
                    if [t.id_teaching for t in teachings].__contains__(t_id):
                        model.add_constraint(x[t1.id_teaching, s] + x[t_id, s] <= 1)

    # Constraint: limiting the number of consecutive lecture slots (max 4 consecutive slots). I only consider the lectures that cannot overlap with each other, since this means that they are in the same Orientation
    # TODO: needs to be tested with the complete DB
    for s in range(len(slots) - (params.max_consecutive_slots + 1)):  # The -5 is used to avoid errors on the last slots
        # The following if is needed to separate the slots between days. Each day has slot_per_day Slots, I don't need to apply a constraint between Monday 17:30-19:00 and Tuesday 8:30-10:00
        if s % params.slot_per_day < params.slot_per_day - params.max_consecutive_slots:
            for t in teachings:
                teachings_in_same_orientation = [t.id_teaching] + list(t.correlations.keys())
                model.add(model.sum(x[to, s + i] for i in range(0, params.max_consecutive_slots+1) for to in teachings_in_same_orientation if to in [teac.id_teaching for teac in teachings]) <= params.max_consecutive_slots)

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
            print(f"{t.id_teaching}: {[int(solution[x[t.id_teaching, s]]) for s in slots]}")
    else:
        print("No solution found.")