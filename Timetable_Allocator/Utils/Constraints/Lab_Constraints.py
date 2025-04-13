'''
    In this file there are the functions needed to add the Constraints about Lab Slots to the model
'''
from Utils.Parameters import Parameters

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_lab(model, timetable_matrix, teaching, slots):
    if teaching.lab_slots != 0:
        # Considering the Groups for Lab Slots
        for i in range(1, teaching.n_weekly_groups_lab):
            # The number of Slots that I need to allocate depends on teaching.double_slots_lab. If 1, I have to allocate blocks of 2 Slots, otherwise I allocate blocks of 1 Slot
            model.add_constraint(
                model.sum(timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] for s in slots)
                == teaching.n_blocks_lab * (2 if teaching.double_slots_lab != 0 else 1))

def add_double_slots_constraint_lab(model, timetable_matrix, teaching, s, d, n_slots_in_day_teaching):
    for i in range(1, teaching.n_lab_groups + 1):
        # Same as above, but for Lab Slots
        if teaching.double_slots_lab != 0 and teaching.lab_slots >= 2:
            model.add(
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] == 0,
                    (
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] +
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s + 1]
                    )
                    == 2
                )
            )
        else:
            if teaching.lab_slots > 0:
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] == 0,
                    (
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] +
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s + 1]
                    )
                    >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d])
                )

'''
    Defines variable n_slots_in_day_teaching which contains the number of Slots in a day for each Lab Group
'''
def define_double_slots_in_day_lab(model, teaching, d, n_slots_in_day_teaching):
    params = Parameters()

    if teaching.lab_slots != 0:
        for i in range(1, teaching.n_lab_groups + 1):
            n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d] = model.integer_var(0, params.max_consecutive_slots_teaching, name=f"y_{teaching.id_teaching + '_lab_group' + str(i)}_{d}")

'''
    Adds the number of Lab Slots in a day to the variable n_slots_in_day_teaching
'''
def count_double_slots_in_day_lab(model, timetable_matrix, teaching, d, n_slots_in_day_teaching):
    params = Parameters()

    if teaching.lab_slots != 0:
        for i in range(1, teaching.n_lab_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d] ==
                model.sum
                (
                    timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s]
                    for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day)
                )
            )

'''
    Constraint: a Teaching cannot overlap with the others, according to the correlations
'''
def add_lab_overlaps_constraint(model, timetable_matrix, t1, t2, s):
    if t1.lab_slots != 0:
        for i in range(1, t1.n_lab_groups + 1):
            model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching, s] <= 1)
            # TODO: add the constraint that a Lab cannot overlap with the same group of a Practice of the same lecture
            # Note: Lab Lectures can not overlap with the same group of Practice Lecture of another Teaching (e.g. Group1 of Lab TeachingA can not overlap with Group1 of Practice TeachingB, but Group1 of Lab TeachingA CAN overlap with Group2 of Practice TeachingB
            if t2.practice_slots != 0 and i <= t2.n_practice_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching + f"_practice_group{i}", s] <= 1)
            # Note: the same Groups of Lab Lectures can not overlap (e.g. Group1 of TeachingA can not overlap with Group1 of TeachingB, but Group1 of TeachingA CAN overlap with Group1 of TeachingB
            if t2.lab_slots != 0 and i <= t2.n_lab_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching + f"_lab_group{i}", s] <= 1)