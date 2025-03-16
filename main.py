import math

from docplex.mp.model import Model
from Components.Slots import get_slots_per_week
from Utils.Hooks.Teachings import Teachings

if __name__ == '__main__':
    # Problem definition
    model = Model(name="PoliTO_Timetable_Scheduling")

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
                    # TODO: cannot test until I can work with the whole DB
                    model.add_constraint(x[t1.id_teaching, s] + x[t_id, s] <= 1)

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
            print(f"{t.id_teaching}: {[int(solution[x[t.id_teaching, s]]) for s in slots]}")
    else:
        print("No solution found.")