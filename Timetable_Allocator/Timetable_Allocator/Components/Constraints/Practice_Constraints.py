'''
    In this file there are the functions needed to add the Constraints about Practice Slots to the model
'''
from Timetable_Allocator.Components.Models.Teaching import Teaching

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_practice(model, timetable_matrix, teaching, slots):
    if teaching.practice_slots != 0:
        # Considering the Groups for Practice Slots
        for i in range(1, teaching.n_practice_groups + 1):
            model.add_constraint(
                model.sum(timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] for s in slots)
                == teaching.practice_slots
            )

'''
    Add the constraint that a Teaching should have a maximum of max_consecutive_slots Slots in a day
'''
def add_max_consecutive_slots_constraint_practice(model, teaching, d, n_slots_in_day_teaching, params):
    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] <= params.max_consecutive_slots_teaching)

'''
    Add the constraint that if n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
'''
def add_double_slots_constraint_practice(model, timetable_matrix, teaching: Teaching, s, d, n_slots_in_day_teaching, teacher_preferences_respected):
    for i in range(1, teaching.n_practice_groups + 1):
        # If teaching.n_min_double_slots_practice >= 1, then I impose that the Teaching must have at leat 2 consecutive practice hours
        # I check that there are at least 2 Slots of practice (to be sure that I can have 2 consecutive Slots)
        if teaching.practice_slots >= teaching.n_min_double_slots_practice + 1 and teaching.practice_slots % 2 == 0 and teaching.n_min_double_slots_practice == 1 and teaching.n_min_single_slots_practice == 0:
            model.add(
                teacher_preferences_respected[teaching.id_teaching + f"_practice_group{i}", d] == (
                    (timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] == 0) |
                    (
                        (timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] +
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1])
                    == 2)
                )
            )

        if teaching.practice_slots > 0:
            model.add(
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] == 0,
                    (
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] +
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1]
                    )
                    >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d])
                )
            )

'''
    Constraint: if the Practice Lecture has to have at least 1 double Slot, then I impose that condition
'''
def add_min_double_slots_contraint_practice(model, teaching, days, double_slots_in_day, teacher_preferences_respected):
    if teaching.n_min_double_slots_practice >= 1 and teaching.practice_slots >= 2:
        for i in range(1, teaching.n_practice_groups + 1):
            for d in days:
                model.add(teacher_preferences_respected[teaching.id_teaching + f"_practice_group{i}", d] >= double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d])

'''
    Defines the variables n_slots_in_day_teaching and double_slots_in_day which contain the number of Practice Slots in a day and days with double Practice Slots
'''
def define_double_slots_in_day_practice(model, teaching, d, n_slots_in_day_teaching, double_slots_in_day, teacher_preferences_respected, params):

    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] = model.integer_var(0, params.max_consecutive_slots_teaching, name=f"n_slots_in_day_teaching_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")
            double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")
            teacher_preferences_respected[teaching.id_teaching + f"_practice_group{i}", d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")

'''
    Adds the number of Practice Slots in a day to the variable n_slots_in_day_teaching
'''
def count_double_slots_in_day_practice(model, timetable_matrix, slots, teaching, d, n_slots_in_day_teaching, params):

    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] ==
                model.sum
                (
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s]
                    for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots
                )
            )

'''
    Adds the Days with at least 2 Practice Slots to the variable double_slots_in_day
'''
def count_days_with_double_slots_practice(model, teaching, d, n_slots_in_day_teaching, double_slots_in_day):
    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            model.add(
                n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] >=
                2 * double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d]
            )

'''
    Constraint: different groups of Practice lectures can not overlap with each other
    Constraint: a Practice cannot overlap with the same group of a Lab of the same lecture
'''
def add_practice_group_constraint(model, timetable_matrix, t1, s, params):
    if t1.practice_slots != 0:
        # Constraint: different groups of Practice lectures can not overlap with each other
        if params.no_overlap_groups:
            for i in range(1, t1.n_practice_groups + 1):
                for j in range(1, i):
                    model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[
                        t1.id_teaching + f"_practice_group{j}", s] <= 1)

        # Constraint: a Practice cannot overlap with the same group of a Lab of the same lecture
        if t1.n_blocks_lab != 0:
            if t1.n_practice_groups == 1:
                for i in range(1, t1.n_lab_groups + 1):
                    model.add(
                        timetable_matrix[t1.id_teaching + "_practice_group1", s] +
                        timetable_matrix[t1.id_teaching + "_lab_group" + str(i), s]
                        <= 1
                    )
            else:
                if t1.n_lab_groups == 1:
                    for i in range(1, t1.n_practice_groups + 1):
                        model.add(
                            timetable_matrix[t1.id_teaching + "_practice_group" + str(i), s] +
                            timetable_matrix[t1.id_teaching + "_lab_group1", s]
                            <= 1
                        )
                else:
                    for i in range(1, min(t1.n_practice_groups, t1.n_lab_groups) + 1):
                        model.add(
                            timetable_matrix[t1.id_teaching + "_practice_group" + str(i), s] +
                            timetable_matrix[t1.id_teaching + "_lab_group" + str(i), s]
                            <= 1
                        )

'''
    Constraint: a Teaching cannot overlap with the others, according to the correlations
'''
def add_practice_overlaps_constraint(model, timetable_matrix, t1, t2, s):
    if t1.practice_slots != 0:
        for i in range(1, t1.n_practice_groups + 1):
            model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[t2.id_teaching, s] <= 1)

            # Note: the same Groups of Practice Lectures can not overlap (e.g. Group1 of TeachingA can not overlap with Group1 of TeachingB, but Group1 of TeachingA CAN overlap with Group2 of TeachingB
            if t2.practice_slots != 0 and i <= t2.n_practice_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[t2.id_teaching + f"_practice_group{i}", s] <= 1)
            # Note: Practice Lectures can not overlap with the same group of Lab Lecture of another Teaching (e.g. Group1 of Practice TeachingA can not overlap with Group1 of Lab TeachingB, but Group1 of Practice TeachingA CAN overlap with Group2 of Lab TeachingB
            if t2.n_blocks_lab != 0 and i <= t2.n_lab_groups and t1.id_teaching < t2.id_teaching:
                model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[t2.id_teaching + f"_lab_group{i}", s] <= 1)

def add_consecutive_groups_slots_constraint_practice(model, timetable_matrix, teaching, s, consecutive_groups_slots):
    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            consecutive_groups_slots[teaching.id_teaching + f"_practice_group{i}", s] = model.binary_var(name=f"consecutive_groups_{teaching.id_teaching + '_practice_group' + str(i)}_{s}")
            for j in range(1, i):
                model.add(consecutive_groups_slots[teaching.id_teaching + f"_practice_group{i}", s] == model.max(
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] * timetable_matrix[teaching.id_teaching + f"_practice_group{j}", s + 1],
                    timetable_matrix[teaching.id_teaching + f"_practice_group{j}", s] * timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1]
                    )
                )

    '''
    Constraint: limiting the number of correlated lectures in a day
'''
def add_correlations_constraint_practice(model, timetable_matrix, slots, t1, s, teaching_ids, params):

    if t1.practice_slots != 0:
        for i in range(1, t1.n_practice_groups + 1):
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] * timetable_matrix[
                    t_id, s + slot_offset])
                for slot_offset in range(1, params.slot_per_day - (s % params.slot_per_day)) if s + slot_offset in slots
                for t_id, (corr, mandatory) in teaching_ids.items()) <= params.max_corr_in_day)

'''
    Define the variables that manage the lectures dispersion in a day
'''
def define_lecture_dispersion_variables_practice(model, slots, t, d, first_lecture_of_day, last_lecture_of_day, lectures_dispersion_of_day, params):

    if t.practice_slots != 0:
        for i in range(1, t.n_practice_groups + 1):
            first_lecture_of_day[t.id_teaching + f"_practice_group{i}", d] = model.integer_var(0, len(slots) - 1, name=f"first_lecture_{t.id_teaching + '_practice_group' + str(i)}_{d}")
            last_lecture_of_day[t.id_teaching + f"_practice_group{i}", d] = model.integer_var(0, len(slots) - 1, name=f"last_lecture_{t.id_teaching + '_practice_group' + str(i)}_{d}")
            lectures_dispersion_of_day[t.id_teaching + f"_practice_group{i}", d] = model.integer_var(0, params.slot_per_day - 1, name=f"lecture_dispersion_{t.id_teaching + '_practice_group' + str(i)}_{d}")

'''
    Assign first and last Slot of Day for each Teaching
'''
def assign_first_last_slot_of_day_practice(model, timetable_matrix, slots, t, d, teaching_ids, first_lecture_of_day, last_lecture_of_day, params):

    if t.practice_slots != 0:
        for i in range(1, t.n_practice_groups + 1):
            model.add(first_lecture_of_day[t.id_teaching + f"_practice_group{i}", d] <= model.max(s * model.max(timetable_matrix[t_id, s]
                for t_id, (corr, mandatory) in teaching_ids.items())
                for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots))
            model.add(last_lecture_of_day[t.id_teaching + f"_practice_group{i}", d] >= model.max(s * model.max(timetable_matrix[t_id, s]
                for t_id, (corr, mandatory) in teaching_ids.items())
                for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day) if s in slots))

'''
    Calculate lecture dispersion as fisrt_slot - last_slot
'''
def calculate_lecture_dispersion_practice(model, t, d, first_lecture_of_day, last_lecture_of_day, lectures_dispersion_of_day):
    if t.practice_slots != 0:
        for i in range(1, t.n_practice_groups + 1):
            model.add(lectures_dispersion_of_day[t.id_teaching + f"_practice_group{i}", d] == last_lecture_of_day[t.id_teaching + f"_practice_group{i}", d] - first_lecture_of_day[t.id_teaching + f"_practice_group{i}", d])

'''
    Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
'''
def add_first_last_slot_correlation_limit_practice(model, timetable_matrix, slots, t1, t2_id, corr, params):

    if t1.practice_slots != 0:
        for i in range(1, t1.n_practice_groups + 1):
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] * timetable_matrix[t2_id, s + (params.slot_per_day - 1)])
                for s in range(0, len(slots), 7) if s + (params.slot_per_day - 1) in slots) <= params.max_corr_first_last_slot)