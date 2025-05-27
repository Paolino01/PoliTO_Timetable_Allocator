'''
    In this file there are the functions needed to add the Constraints about Lab Slots to the model
'''
from Utils.Parameters import Parameters

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_lab(model, timetable_matrix, teaching, slots):
    if teaching.n_blocks_lab != 0:
        # Considering the Groups for Lab Slots
        for i in range(1, teaching.n_lab_groups+1):
            # The number of Slots that I need to allocate depends on teaching.double_slots_lab. If 1, I have to allocate blocks of 2 Slots, otherwise I allocate blocks of 1 Slot
            model.add_constraint(
                model.sum(timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] for s in slots)
                == teaching.n_blocks_lab * (2 if teaching.double_slots_lab != 0 else 1))

'''
    Add the constraint that a Teaching should have a maximum of max_consecutive_slots Slots in a day
'''
def add_max_consecutive_slots_constraint_lab(model, teaching, d, max_consecutive_slots, n_slots_in_day_teaching):
    if teaching.n_blocks_lab != 0:
        for i in range(1, teaching.n_lab_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d] <= max_consecutive_slots)

'''
    Add the constraint that if n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
'''
def add_double_slots_constraint_lab(model, timetable_matrix, teaching, s, d, n_slots_in_day_teaching, teacher_preferences_respected):
    for i in range(1, teaching.n_lab_groups + 1):
        # Same as Practice, but for Lab Slots
        # I don't check Lab Slots since I don't use them (I set the number of Slots in add_slots_per_week_lab)

        # TODO: needs review and testing
        if teaching.double_slots_lab != 0 and teaching.double_slots_lab == 1:
            model.add(
                teacher_preferences_respected[teaching.id_teaching + f"_lab_group{i}", d] == (
                    (timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] == 0) |
                    (
                        (timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] +
                        timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s + 1])
                    == 2)
                )
            )

        if teaching.n_blocks_lab > 0:
            model.add(
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] == 0,
                    (
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] +
                            timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s + 1]
                    )
                    >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d])
                )
            )

'''
    Defines variable n_slots_in_day_teaching which contains the number of Slots in a day for each Lab Group
'''
def define_double_slots_in_day_lab(model, teaching, d, n_slots_in_day_teaching, teacher_preferences_respected, params):

    if teaching.n_blocks_lab != 0:
        for i in range(1, teaching.n_lab_groups + 1):
            n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d] = model.integer_var(0, params.max_consecutive_slots_teaching, name=f"y_{teaching.id_teaching + '_lab_group' + str(i)}_{d}")
            teacher_preferences_respected[teaching.id_teaching + f"_lab_group{i}", d] = model.binary_var(name=f"y_{teaching.id_teaching + '_lab_group' + str(i)}_{d}")

'''
    Adds the number of Lab Slots in a day to the variable n_slots_in_day_teaching
'''
def count_double_slots_in_day_lab(model, timetable_matrix, slots, teaching, d, n_slots_in_day_teaching, params):

    if teaching.n_blocks_lab != 0:
        for i in range(1, teaching.n_lab_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_lab_group{i}", d] ==
                model.sum
                (
                    timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s]
                    for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots
                )
            )

'''
    Constraint: different groups of Lab lectures can not overlap with each other
'''
def add_lab_group_constraint(model, timetable_matrix, t1, s):
    # TODO: needs to be tested
    if t1.n_blocks_lab != 0:
        for i in range(1, t1.n_lab_groups + 1):
            for j in range(1, i):
                model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t1.id_teaching + f"_lab_group{j}", s] <= 1)

'''
    Constraint: a Teaching cannot overlap with the others, according to the correlations
'''
def add_lab_overlaps_constraint(model, timetable_matrix, t1, t2, s):
    if t1.n_blocks_lab != 0:
        for i in range(1, t1.n_lab_groups + 1):
            model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching, s] <= 1)

            # Note: Lab Lectures can not overlap with the same group of Practice Lecture of another Teaching (e.g. Group1 of Lab TeachingA can not overlap with Group1 of Practice TeachingB, but Group1 of Lab TeachingA CAN overlap with Group2 of Practice TeachingB
            if t2.practice_slots != 0 and i <= t2.n_practice_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching + f"_practice_group{i}", s] <= 1)
            # Note: the same Groups of Lab Lectures can not overlap (e.g. Group1 of TeachingA can not overlap with Group1 of TeachingB, but Group1 of TeachingA CAN overlap with Group1 of TeachingB
            if t2.n_blocks_lab != 0 and i <= t2.n_lab_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] + timetable_matrix[t2.id_teaching + f"_lab_group{i}", s] <= 1)

'''
    Constraint: limiting the number of correlated lectures in a day
'''
def add_correlations_constraint_lab(model, timetable_matrix, slots, t1, s, teaching_ids, params):

    if t1.n_blocks_lab != 0:
        for i in range(1, t1.n_lab_groups + 1):
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] * timetable_matrix[
                    t_id, s + slot_offset])
                for slot_offset in range(1, params.slot_per_day - (s % params.slot_per_day)) if s + slot_offset in slots
                for t_id, (corr, mandatory) in teaching_ids.items()) <= params.max_corr_in_day)

'''
    Define the variables that manage the lectures dispersion in a day
'''
def define_lecture_dispersion_variables_lab(model, slots, t, d, first_lecture_of_day, last_lecture_of_day, lectures_dispersion_of_day, params):

    if t.n_blocks_lab != 0:
        for i in range(1, t.n_lab_groups + 1):
            first_lecture_of_day[t.id_teaching + f"_lab_group{i}", d] = model.integer_var(0, len(slots) - 1, name=f"first_lecture_{t.id_teaching + '_lab_group' + str(i)}_{d}")
            last_lecture_of_day[t.id_teaching + f"_lab_group{i}", d] = model.integer_var(0, len(slots) - 1, name=f"last_lecture_{t.id_teaching + '_lab_group' + str(i)}_{d}")
            lectures_dispersion_of_day[t.id_teaching + f"_lab_group{i}", d] = model.integer_var(0, params.slot_per_day - 1, name=f"lecture_dispersion_{t.id_teaching + '_lab_group' + str(i)}_{d}")

'''
    Assign first and last Slot of Day for each Teaching
'''
def assign_first_last_slot_of_day_lab(model, timetable_matrix, slots, t, d, teaching_ids, first_lecture_of_day, last_lecture_of_day, params):

    if t.n_blocks_lab != 0:
        for i in range(1, t.n_lab_groups + 1):
            model.add(first_lecture_of_day[t.id_teaching + f"_lab_group{i}", d] <= model.max(s * model.max(timetable_matrix[t_id, s]
                for t_id, (corr, mandatory) in teaching_ids.items())
                for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots))
            model.add(last_lecture_of_day[t.id_teaching + f"_lab_group{i}", d] >= model.max(s * model.max(timetable_matrix[t_id, s]
                for t_id, (corr, mandatory) in teaching_ids.items())
                for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots))

'''
    Calculate lecture dispersion as fisrt_slot - last_slot
'''
def calculate_lecture_dispersion_lab(model, t, d, first_lecture_of_day, last_lecture_of_day, lectures_dispersion_of_day):
    if t.n_blocks_lab != 0:
        for i in range(1, t.n_lab_groups + 1):
            model.add(lectures_dispersion_of_day[t.id_teaching + f"_lab_group{i}", d] == last_lecture_of_day[t.id_teaching + f"_lab_group{i}", d] - first_lecture_of_day[t.id_teaching + f"_lab_group{i}", d])

'''
    Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
'''
def add_first_last_slot_correlation_limit_lab(model, timetable_matrix, slots, t1, t2_id, corr, params):

    if t1.n_blocks_lab != 0:
        for i in range(1, t1.n_lab_groups + 1):
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching + f"_lab_group{i}", s] * timetable_matrix[t2_id, s + (params.slot_per_day - 1)])
                for s in range(0, len(slots), 7) if s + (params.slot_per_day - 1) in slots) <= params.max_corr_first_last_slot)