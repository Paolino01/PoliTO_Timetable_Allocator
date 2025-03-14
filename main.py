from docplex.mp.model import Model
from slots import Slots

if __name__ == '__main__':
    # Problem definition
    model = Model(name="PoliTO_Timetable_Scheduling")

    s = Slots()

    # List of Teachings that I need to allocate
    subjects = ["Math", "CS", "Physics"]

    #Number of slots per week
    slots = s.getSlotsPerWeek()

    # Variabili binarie x[s,t] = 1 se la materia 's' è assegnata allo slot 't'
    x = {(s, t): model.binary_var(name=f"x_{s}_{t}") for s in subjects for t in slots}

    # Vincolo: ogni materia deve avere esattamente 2 lezioni a settimana
    for s in subjects:
        model.add_constraint(model.sum(x[s, t] for t in slots) == 2)

    # Vincolo: in ogni slot può esserci al massimo una materia
    for t in slots:
        model.add_constraint(model.sum(x[s, t] for s in subjects) <= 1)

    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for s in subjects:
            print(f"{s}: {[int(solution[x[s, t]]) for t in slots]}")
    else:
        print("No solution found.")