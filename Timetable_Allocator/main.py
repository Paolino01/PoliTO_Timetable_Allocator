import math
from docplex.cp.model import CpoModel
from Components.Slots import get_slots_per_week
from Data.DbAPI import DbAPI
from Utils.Constraints.Teacher_Constraints import add_teachers_constraints
from Utils.Constraints.Teaching_Constraints import add_teachings_constraints
from Utils.Hooks.Teachers import Teachers
from Utils.Hooks.Teachings import Teachings
from Utils.Parameters import Parameters

if __name__ == '__main__':
    # Problem definition
    model = CpoModel(name="PoliTO_Timetable_Scheduling")

    params = Parameters()
    db_api = DbAPI()

    # List of Teachings that I need to allocate
    teachings_class = Teachings()
    teachings = teachings_class.teachings

    # List of Teachers with their Teachings
    teachers_class = Teachers(teachings)
    teachers = teachers_class.teachers

    # Number of slots per week
    slots = get_slots_per_week()
    # Number of days per week
    days = range(5 if params.saturday_enabled == False else 6)

    '''Variables for the model'''
    # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
    timetable_matrix = dict()
    for t in teachings:
        for s in slots:
            timetable_matrix[(t.id_teaching, s)] = model.binary_var(name=f"x_{t.id_teaching}_{s}")

            '''
            if t.lab_hours != 0:
                timetable_matrix[(t.id_teaching + '_lab', s)] = model.binary_var(name=f"x_{t.id_teaching + '_lab'}_{s}")
            '''


    '''Teachings Constraints'''
    add_teachings_constraints(model, timetable_matrix, teachings, slots, days)


    '''Teachers Contraints'''
    add_teachers_constraints(model, timetable_matrix, teachers, slots, days)


    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for t in teachings:
            print(f"{t.id_teaching}: {[int(solution[timetable_matrix[t.id_teaching, s]]) for s in slots]}")
            '''
            if t.lab_hours != 0:
                lab_id = t.id_teaching + "_lab"
                print(f"{lab_id}: {[int(solution[timetable_matrix[lab_id, s]]) for s in slots]}")
            '''

        # Saving the results to the DB
        db_api.save_results_to_db(solution, timetable_matrix, slots, teachings)
    else:
        print("\nNo solution found.")