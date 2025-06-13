from docplex.cp.model import CpoModel

from Components.Export_to_Excel import export_solution_to_excel
from Components.Generated_Solution import add_generated_courses
from Components.Previous_Solution import get_previous_solution, ask_previous_solution
from Components.Slots import get_slots_per_week
from Data.DbAPI import DbAPI
from Utils.Constraints.Teacher_Constraints import add_teachers_constraints
from Utils.Constraints.Teaching_Constraints import add_teachings_constraints
from Utils.Hooks.Teachers import Teachers
from Utils.Hooks.Teachings import Teachings
from Utils.Parameters import Parameters

if __name__ == '__main__':
    params = Parameters()
    db_api = DbAPI(params)

    # Number of slots per week
    slots = get_slots_per_week(params)
    # Number of days per week
    days = range(5 if params.saturday_enabled == False else 6)

    # Ask the user if they want to start from an existing solution
    ask_previous_solution(params)

    teachings_class = Teachings(params)

    solution_found = True

    for i in range(0, len(params.course_order)):
        print("Generating timetable for " + str(params.course_order[i]["courses"]))

        # Problem definition
        model = CpoModel(name="PoliTO_Timetable_Scheduling")

        # List of Teachings that I need to allocate
        teachings_class.load_teachings_from_db(params.course_order[i], params)
        teachings = teachings_class.teachings_list
    
        # List of Teachers with their Teachings
        teachers_class = Teachers(teachings, params)
        teachers = teachers_class.teachers_list

        '''Variables for the model'''
        # Binary variables timetable_matrix[t,s] = 1 if the Teaching 't' is assigned to Slot 's'
        timetable_matrix = dict()
        for teaching in teachings:
            for s in slots:
                timetable_matrix[(teaching.id_teaching, s)] = model.binary_var(name=f"timetable_matrix_{teaching.id_teaching}_{s}")
    
                if teaching.practice_slots != 0:
                    for practice_group in range(1, teaching.n_practice_groups + 1):
                        timetable_matrix[(teaching.id_teaching + f"_practice_group{practice_group}", s)] = model.binary_var(name=f"x_{teaching.id_teaching + '_practice_group' + str(practice_group)}_{s}")
                if teaching.n_blocks_lab != 0:
                    for lab_group in range(1, teaching.n_lab_groups + 1):
                        timetable_matrix[(teaching.id_teaching + f"_lab_group{lab_group}", s)] = model.binary_var(name=f"x_{teaching.id_teaching + '_lab_group' + str(lab_group)}_{s}")

        # If the user wants to start from a previous solution, load it from the DB
        get_previous_solution(model, timetable_matrix, teachings, slots, params)
    
        # Add courses of an already generated timetable
        if i != 0:
            add_generated_courses(model, timetable_matrix, slots, params)

        # Set parameters according to the the current course generation schema
        params.max_corr_in_day = params.course_order[i]["max_corr_in_day"]
        params.max_corr_first_last_slot = params.course_order[i]["max_corr_first_last_slot"]
        params.min_corr_overlaps = params.course_order[i]["min_corr_overlaps"]
        params.no_overlap_mandatory_practice_lab = params.course_order[i]["no_overlap_mandatory_practice_lab"]
        params.no_overlap_groups = params.course_order[i]["no_overlap_groups"]
        params.teachers_unavailabilities = params.course_order[i]["teachers_unavailabilities"]

        '''Teachings Constraints'''
        add_teachings_constraints(model, timetable_matrix, teachings, slots, days, params)

        '''Teachers Contraints'''
        add_teachers_constraints(model, timetable_matrix, teachers, slots, params)

        solution = model.solve(log_output=True)
    
        # Printing the results
        if solution:
            print("\nSolution found:")
            for teaching in teachings:
                print(f"{teaching.id_teaching}: {[int(solution[timetable_matrix[teaching.id_teaching, s]]) for s in slots]}")
    
                if teaching.practice_slots != 0:
                    for i in range(1, teaching.n_practice_groups + 1):
                        print(f"{teaching.id_teaching + '_practice_group' + str(i)}: {[int(solution[timetable_matrix[teaching.id_teaching + '_practice_group' + str(i), s]]) for s in slots]}")
    
                if teaching.n_blocks_lab != 0:
                    for i in range(1, teaching.n_lab_groups + 1):
                        print(f"{teaching.id_teaching + '_lab_group' + str(i)}: {[int(solution[timetable_matrix[teaching.id_teaching + '_lab_group' + str(i), s]]) for s in slots]}")
    
            # Saving the results to the DB
            db_api.save_results_to_db(solution, timetable_matrix, slots, teachings, teachers, params)
        else:
            print("\nNo solution found.")
            solution_found = False
            break

    if solution_found:
        # Solution found, I delete the previous solution with the same name and save this one
        db_api.remove_solution(params.timetable_name)
        db_api.rename_temp_solution(params)

        print("\nTimetable generated successfully.")

        print("Do you want to export the solution to an Excel file (y/n)?")
        if input().lower() == "y":
            export_solution_to_excel(params)
    else:
        # No solution found, I ask the user if they want to keep or delete the partial results
        print("No solution found, would you like to delete the partial results of this execution from the database (y/n)?")
        if input().lower() == "y":
            db_api.remove_solution(params.timetable_name + "_temp")
            print("DB cleaned")
