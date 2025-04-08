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
    teachings = teachings_class.teachings_list

    # List of Teachers with their Teachings
    teachers_class = Teachers(teachings)
    teachers = teachers_class.teachers_list

    # Number of slots per week
    slots = get_slots_per_week()
    # Number of days per week
    days = range(5 if params.saturday_enabled == False else 6)

    '''Variables for the model'''
    # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
    timetable_matrix = dict()
    for teaching in teachings:
        for s in slots:
            timetable_matrix[(teaching.id_teaching, s)] = model.binary_var(name=f"x_{teaching.id_teaching}_{s}")

            if teaching.practice_slots != 0:
                for i in range(1, teaching.n_practice_groups + 1):
                    timetable_matrix[(teaching.id_teaching + f"_practice_group{i}", s)] = model.binary_var(name=f"x_{teaching.id_teaching + '_practice_group' + str(i)}_{s}")
            if teaching.lab_slots != 0:
                for i in range(1, teaching.n_lab_groups + 1):
                    timetable_matrix[(teaching.id_teaching + f"_lab_group{i}", s)] = model.binary_var(name=f"x_{teaching.id_teaching + '_lab_group' + str(i)}_{s}")


    '''Teachings Constraints'''
    add_teachings_constraints(model, timetable_matrix, teachings, slots, days)


    '''Teachers Contraints'''
    add_teachers_constraints(model, timetable_matrix, teachers, slots, days)


    # Solving the problem
    solution = model.solve(log_output=True)

    # Printing the results
    if solution:
        print("\nSolution found:")
        for teaching in teachings:
            print(f"{teaching.id_teaching}: {[int(solution[timetable_matrix[teaching.id_teaching, s]]) for s in slots]}")

            if teaching.practice_slots != 0:
                for i in range(1, teaching.n_practice_groups + 1):
                    print(f"{teaching.id_teaching + '_practice_group' + str(i)}: {[int(solution[timetable_matrix[teaching.id_teaching + '_practice_group' + str(i), s]]) for s in slots]}")
            '''
            if t.lab_hours != 0:
                lab_id = t.id_teaching + "_lab"
                print(f"{lab_id}: {[int(solution[timetable_matrix[lab_id, s]]) for s in slots]}")
            '''

        # Saving the results to the DB
        db_api.save_results_to_db(solution, timetable_matrix, slots, teachings)
    else:
        print("\nNo solution found.")