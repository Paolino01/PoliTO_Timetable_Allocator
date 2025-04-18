from Data.DbAPI import DbAPI
from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


def get_previous_solution(model, timetable_matrix: dict, teachings: list[Teaching], slots: range):
    params = Parameters()
    db_api = DbAPI()

    print("Do you want to start from an existing solution? (y/n): ")
    params.start_from_previous_solution = input().lower() == "y"
    if params.start_from_previous_solution:
        previous_solution_string = db_api.get_previous_solution()

        previous_solution = {}
        for row in previous_solution_string:
            for s in slots:
                if row[2] == "L":
                    previous_solution[str(row[1]), s] = 1 if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s else 0
                else:
                    if row[5] == "No squadra":
                        lect_group = 1
                    else:
                        lect_group = int(row[5].split(' ')[1])

                    if row[2] == "EA":
                        previous_solution[str(row[1]) + f"_practice_group{lect_group}", s] = 1 if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s else 0
                    else:
                        if row[2] == "EL":
                            previous_solution[str(row[1]) + f"_lab_group{lect_group}", s] = 1 if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s else 0

        start_solution = model.create_empty_solution()
        for t in teachings:
            for s in slots:
                start_solution[timetable_matrix[t.id_teaching, s]] = previous_solution.get((t.id_teaching, s), 0)
                if t.practice_slots != 0:
                    for i in range(1, t.n_practice_groups + 1):
                        start_solution[timetable_matrix[t.id_teaching + f"_practice_group{i}", s]] = previous_solution.get((t.id_teaching + f"_practice_group{i}", s), 0)

                if t.n_blocks_lab != 0:
                    for i in range(1, t.n_lab_groups + 1):
                        start_solution[timetable_matrix[t.id_teaching + f"_lab_group{i}", s]] = previous_solution.get((t.id_teaching + f"_lab_group{i}", s), 0)


        model.set_starting_point(start_solution)