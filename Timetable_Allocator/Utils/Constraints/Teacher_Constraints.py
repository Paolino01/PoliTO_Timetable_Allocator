'''
    In this file we set the constraints related to the Teachers
'''
from Utils.Parameters import Parameters

'''
    Get the IDs of the Teachings, considering Practices and Labs as well, divided per didactic period
    Returns a list of Teaching IDs
'''
def get_teaching_ids(teacher):
    teaching_ids_1 = []
    teaching_ids_2 = []

    # teaching[0] contains a reference to the Teaching, teaching[1] contains a reference to the lecture type taught by the Teacher
    for teaching in teacher.teachings:
            if teaching[1] == "L":
                if teaching[0].didactic_period[-1] == "1":
                    teaching_ids_1.append(teaching[0].id_teaching)
                elif teaching[0].didactic_period[-1] == "2":
                    teaching_ids_2.append(teaching[0].id_teaching)
            else:
                if teaching[1] == "EA" and teaching[0].practice_slots != 0:
                    for i in range(1, teaching[0].n_practice_groups + 1):
                        if teaching[0].didactic_period[-1] == "1":
                            teaching_ids_1.append(teaching[0].id_teaching + f"_practice_group{i}")
                        elif teaching[0].didactic_period[-1] == "2":
                            teaching_ids_2.append(teaching[0].id_teaching + f"_practice_group{i}")
                else:
                    if teaching[1] == "EL" and teaching[0].n_blocks_lab != 0:
                        for i in range(1, teaching[0].n_lab_groups + 1):
                            if teaching[0].didactic_period[-1] == "1":
                                teaching_ids_1.append(teaching[0].id_teaching + f"_lab_group{i}")
                            elif teaching[0].didactic_period[-1] == "2":
                                teaching_ids_2.append(teaching[0].id_teaching + f"_lab_group{i}")

    return teaching_ids_1, teaching_ids_2

'''
    Teachings with the same Teacher should not overlap
'''
def add_no_overlap_constraint(model, timetable_matrix, teacher, slots):
    # Getting the IDs of the Teachings taught by "teacher" for the first and the second semester
    teaching_ids_1, _teaching_ids_2 = get_teaching_ids(teacher)

    for s in slots:
        # Constraints for the first semester
        model.add(model.sum(timetable_matrix[t_id, s] for t_id in teaching_ids_1) <= 1)

        # Constraints for the second semester
        # model.add(model.sum(timetable_matrix[t_id, s] for t_id in _teaching_ids_2) <= 1)

'''
    A Teacher cannot have lectures in a Slot in which they are unavailable
'''
def add_unavailable_slots_constraint(model, timetable_matrix, teacher):
    for teaching in teacher.teachings:
        for s in teacher.unaivalable_slots:
            if teaching[1] == "L":
                model.add(timetable_matrix[teaching[0].id_teaching, s] == 0)
            else:
                if teaching[1] == "EA" and teaching[0].practice_slots != 0:
                    '''Practice Slots'''
                    for i in range(1, teaching[0].n_practice_groups + 1):
                        model.add(timetable_matrix[teaching[0].id_teaching + f"_practice_group{i}", s] == 0)
                else:
                    if teaching[1] == "EL" and teaching[0].n_blocks_lab != 0:
                        '''Lab Slots'''
                        for i in range(1, teaching[0].n_lab_groups + 1):
                            model.add(timetable_matrix[teaching[0].id_teaching + f"_lab_group{i}", s] == 0)


'''
    Add the constraints for the Teachers to the model
'''
def add_teachers_constraints(model, timetable_matrix, teachers, slots, params):
    for teacher in teachers:
        # Constraint: Teachings taught by the same Teacher cannot overlap
        add_no_overlap_constraint(model, timetable_matrix, teacher, slots)

        # Constraint: a Teacher cannot have lectures in a Slot in which they are unavailable
        if params.teachers_unavailabilities:
            add_unavailable_slots_constraint(model, timetable_matrix, teacher)