from Data.DbAPI import DbAPI
from Utils.Parameters import Parameters

'''
    Get the courses from a previously generated timetable and add them to the model as fixed variables
'''
def add_generated_courses(model, timetable_matrix, slots, params):
    dbapi = DbAPI(params)

    generated_courses_string = dbapi.get_generated_courses(params)

    for row in generated_courses_string:
        for s in slots:
            if row[2] == "L":
                if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s:
                    model.add(timetable_matrix[str(row[1]), s] == 1)
            else:
                if row[5] == "No squadra":
                    lect_group = 1
                else:
                    lect_group = int(row[5][-1])

                if row[2] == "EA":
                    if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s:
                        model.add(timetable_matrix[str(row[1]) + f"_practice_group{lect_group}", s] == 1)
                else:
                    if row[2] == "EL":
                        if (params.days.index(row[3]) * params.slot_per_day + params.time_slots.index(row[4])) == s:
                            model.add(timetable_matrix[str(row[1]) + f"_lab_group{lect_group}", s] == 1)
