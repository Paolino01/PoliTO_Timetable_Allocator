from Utils.Parameters import Parameters

'''
    Teachings with the same Teacher as main Teacher should not overlap
'''
def add_no_overlap_constraint(model, timetable_matrix, teacher, slots):
    for s in slots:
        # Constraints for the first semester
        model.add(
            model.sum(timetable_matrix[teaching.id_teaching, s] for teaching in teacher.teachings if teaching.didactic_period[-1] == '1') <= 1
        )

        # Constraints for the second semester
        model.add(
            model.sum(timetable_matrix[teaching.id_teaching, s] for teaching in teacher.teachings if teaching.didactic_period[-1] == '2') <= 1
        )

'''
    A Teacher cannot have lectures in a Slot in which they are unavailable
'''
def add_unavailable_slots_constraint(model, timetable_matrix, teacher):
    for teaching in teacher.teachings:
        for s in teacher.unaivalable_slots:
            model.add(timetable_matrix[teaching.id_teaching, s] == 0)

'''
    A Teacher cannot have more than params.max_consecutive_slot consecutive Slots
'''
def add_max_consecutive_slots_constraint(model, timetable_matrix, teacher, slots, days):
    params = Parameters()

    for d in days:
        model.add(model.sum(timetable_matrix[teaching.id_teaching, s + i]
            for teaching in teacher.teachings
            for s in range(d * params.slot_per_day, ((d + 1) * params.slot_per_day) - params.max_consecutive_slots_teacher) if s in slots
            for i in range(0, (params.max_consecutive_slots_teacher + 1))
            )
        <= params.max_consecutive_slots_teacher
        )


'''
    Add the constraints for the Teachers to the model
'''
def add_teachers_constraints(model, timetable_matrix, teachers, slots, days):
    for teacher in teachers:
        # Constraint: Teachings taught by the same Teacher cannot overlap
        add_no_overlap_constraint(model, timetable_matrix, teacher, slots)

        # Constraint: a Teacher cannot have lectures in a Slot in which they are unavailable
        add_unavailable_slots_constraint(model, timetable_matrix, teacher)

        # Constraint: a Teacher cannot have more that params.max_consecutive_slots_teacher consecutive Slots of lectures
        add_max_consecutive_slots_constraint(model, timetable_matrix, teacher, slots, days)

