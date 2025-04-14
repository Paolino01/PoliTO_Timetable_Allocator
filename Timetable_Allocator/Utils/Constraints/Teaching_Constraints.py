import math

from Utils.Constraints.Lab_Constraints import add_double_slots_constraint_lab, add_slots_per_week_lab, \
    define_double_slots_in_day_lab, count_double_slots_in_day_lab, add_lab_overlaps_constraint
from Utils.Constraints.Practice_Constraints import add_double_slots_constraint_practice, add_slots_per_week_practice, \
    add_min_double_slots_contraint_practice, define_double_slots_in_day_practice, count_double_slots_in_day_practice, \
    count_days_with_double_slots_practice, add_practice_overlaps_constraint
from Utils.Parameters import Parameters

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_teaching(model, timetable_matrix, teachings, slots):
    for teaching in teachings:
        model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching, s] for s in slots) == teaching.lect_slots)

        '''Practice Slots'''
        add_slots_per_week_practice(model, timetable_matrix, teaching, slots)
                
        '''Lab Slots'''
        add_slots_per_week_lab(model, timetable_matrix, teaching, slots)

'''
    Add the constraint that a Teaching should have a maximum of max_consecutive_slots Slots in a day
'''
def add_max_consecutive_slots_constraint(model, teaching, d, n_slots_in_day_teaching):
    # Assign max consecutive Slots for a lecture according to teaching.n_min_double_slots_lecture
    if teaching.n_min_double_slots_lecture+1 > 2:
        max_consecutive_slots = teaching.n_min_double_slots_lecture+1
    else:
        max_consecutive_slots = 2

    if teaching.n_min_single_slots_lecture > 0 or teaching.n_min_double_slots_lecture == 0:
        model.add(n_slots_in_day_teaching[teaching.id_teaching, d] <= max_consecutive_slots)
    else:
        # If a Teaching can not have at least 1 single slot lecture, then it should only have double Slots

        # Checking that the number of Slots of a Teaching is even, in order to allocate only double Slots
        if teaching.lect_slots % 2 == 0:
            model.add(
                model.logical_or(
                    n_slots_in_day_teaching[teaching.id_teaching, d] == 0,
                    n_slots_in_day_teaching[teaching.id_teaching, d] == max_consecutive_slots
                )
            )
        else:
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] <= max_consecutive_slots)

'''
    Add the constraint that if n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
'''
def add_double_slots_constraint(model, timetable_matrix, slots, teaching, d, n_slots_in_day_teaching):
    params = Parameters()

    for s in range(len(slots) - 1):
        if math.floor(s / params.slot_per_day) == d and math.floor((s + 1) / params.slot_per_day) == d:
            # I consider 2 consecutive Slots. Those Slots should either have no lectures for this Teaching (== 0) or they should have n_slots_in_day_teaching lectures, to be sure that those lectures are consecutive
            model.add(
                model.logical_or(
                    timetable_matrix[teaching.id_teaching, s] == 0,
                    (
                        timetable_matrix[teaching.id_teaching, s] +
                        timetable_matrix[teaching.id_teaching, s + 1]
                    )
                    >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching, d])
                )
            )

            '''Practice Slots'''
            add_double_slots_constraint_practice(model, timetable_matrix, teaching, s, d, n_slots_in_day_teaching)

            '''Lab Slots'''
            add_double_slots_constraint_lab(model, timetable_matrix, teaching, s, d, n_slots_in_day_teaching)

'''
    Constraint: if the Teaching has to have at least 1 double Slot, then I impose that condition
'''
def add_min_double_slots_contraint(model, days, teaching, double_slots_in_day):
    if teaching.n_min_double_slots_lecture >= 1 and teaching.lect_slots >= teaching.n_min_single_slots_lecture + 1:
        model.add(model.sum(double_slots_in_day[teaching.id_teaching, d] for d in days) >= 1)

    '''Practice Slots'''
    # Same as above but for practice
    add_min_double_slots_contraint_practice(model, teaching, days, double_slots_in_day)

'''
    Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive.
    We also take into account the Teacher's preferences about Slot allocations for the Teachings
'''
def add_daily_slots_constraints(model, timetable_matrix, teachings, slots, days):
    # Note: this constraint should only be applied to Lecture Slots and not Laboratory Slots

    params = Parameters()

    # Variable that counts how many hours a teaching has in a day
    n_slots_in_day_teaching = {}

    # double_slots_in_day = 1 if the Lecture/Practice has at least 2 Slots in that Day
    double_slots_in_day = {}
    for teaching in teachings:
        for d in days:
            n_slots_in_day_teaching[teaching.id_teaching, d] = model.integer_var(0, params.max_consecutive_slots_teaching, name=f"y_{teaching.id_teaching}_{d}")
            double_slots_in_day[teaching.id_teaching, d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching}_{d}")

            '''Practice Slots'''
            define_double_slots_in_day_practice(model, teaching, d, n_slots_in_day_teaching, double_slots_in_day)

            '''Lab Slots'''
            define_double_slots_in_day_lab(model, teaching, d, n_slots_in_day_teaching)

    for teaching in teachings:
        for d in days:
            # Counts how many hours the Teaching t has in Day d
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] == model.sum
                (
                    timetable_matrix[teaching.id_teaching, s]
                    for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day)
                )
            )

            '''Practice Slots'''
            count_double_slots_in_day_practice(model, timetable_matrix, teaching, d, n_slots_in_day_teaching)

            '''Lab Slots'''
            count_double_slots_in_day_lab(model, timetable_matrix, teaching, d, n_slots_in_day_teaching)

            # Counting how many days have 2 or more Slots of the same lecture
            model.add(
                n_slots_in_day_teaching[teaching.id_teaching, d] >= 2 * double_slots_in_day[teaching.id_teaching, d]
            )
            '''Practice Slots'''
            count_days_with_double_slots_practice(model, teaching, d, n_slots_in_day_teaching, double_slots_in_day)

            # Add the constraint that a Teaching should have a maximum of max_consecutive_slots Slots in a day (only for Lectures and not for Laboratories)
            add_max_consecutive_slots_constraint(model, teaching, d, n_slots_in_day_teaching)

            # If n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
            add_double_slots_constraint(model, timetable_matrix, slots, teaching, d, n_slots_in_day_teaching)

        # Constraint: if the Teaching has to have at least 1 double Slot, then I impose that condition
        add_min_double_slots_contraint(model, days, teaching, double_slots_in_day)

'''
    Constraint: limiting the number of correlated lectures in a day
    Constraint: a Teaching cannot overlap with the others, according to the correlations
'''
def add_correlations_overlaps_constraint(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for t1 in teachings:
        for s in slots:
            # Constraint: limiting the number of correlated lectures in a day. For example, I impose that the sum of the correlations between lectures in a day should be <= params.max_corr_in_day
            # This way I don't limit the number of consecutive lecture slots
            # Not applying this for the practice lectures and laboratories, since they are probably divided in groups. Need to verify that the timetable generated is good of if we need to apply this constraint to practices and labs as well
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2.id_teaching, s + i])
                for i in range(1, params.slot_per_day - (s % params.slot_per_day)) if s + i in slots
                for t2, corr in t1.correlations.items()) <= params.max_corr_in_day)

            # Constraint: a Teaching cannot overlap with the others, according to the correlations
            for t2, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from TeachingA to TeachingB and the other from TeachingB to TeachingA)
                if t1.id_teaching < t2.id_teaching and corr > 20:
                    model.add(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2.id_teaching, s] <= 1)

                '''Practice Slots'''
                # Adding the constraint to the Practice Slots
                add_practice_overlaps_constraint(model, timetable_matrix, t1, t2, s)

                '''Lab Slots'''
                # Adding the constraint to the Lab Slots
                add_lab_overlaps_constraint(model, timetable_matrix, t1, t2, s)

            # Constraint: a Lab cannot overlap with the same group of a Practice of the same lecture
            if t1.practice_slots != 0 and t1.lab_slots != 0:
                for i in range(1, min(t1.n_practice_groups, t1.n_lab_groups) + 1):
                    model.add(
                        timetable_matrix[t1.id_teaching + "_practice_group" + str(i), s] +
                        timetable_matrix[t1.id_teaching + "_lab_group" + str(i), s]
                        <= 1
                    )

'''
    Constraint: I consider params.n_consecutive_slots consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
'''
def add_consecutive_slots_constraint(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for s in range(len(slots) - (params.n_consecutive_slots - 1)):
        for t1 in teachings:
            # Not applying this for the practice lectures and laboratories, since they are probably divided in groups. Need to verify that the timetable generated is good of if we need to apply this constraint to practices and labs as well
            correlations_in_slots = model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2.id_teaching, s + i])
                for i in range(1, params.n_consecutive_slots)
                for t2, corr in t1.correlations.items())

            model.add(1 == model.logical_or(correlations_in_slots == 0, correlations_in_slots >= params.min_corr_in_slots))

'''
    Constraint: the difference between the first and last lecture slot of the day should be minimized
'''
def add_first_last_lecture_of_day_limit(model, timetable_matrix, teachings, slots, days):
    params = Parameters()

    # Variables that save the first and last lecture Slots, for each Day and Teaching
    first_lecture_of_day = {
        (teaching.id_teaching, d): model.integer_var(0, len(slots) - 1, name=f"first_lecture_{teaching.id_teaching}_{d}")
        for teaching in teachings for d in days
    }
    last_lecture_of_day = {
        (teaching.id_teaching, d): model.integer_var(0, len(slots) - 1, name=f"last_lecture_{teaching.id_teaching}_{d}")
        for teaching in teachings for d in days
    }
    # Variable that saves the difference between the first and last lecture Slot, for each Day and Teaching
    lectures_dispersion_of_day = {(t.id_teaching, d): model.integer_var(0, params.slot_per_day - 1, name=f"lecture_dispersion_{t.id_teaching}_{d}") for t in teachings for d in days}

    # Not applying this for the practice lectures and laboratories, since they are probably divided in groups. Need to verify that the timetable generated is good of if we need to apply this constraint to practices and labs as well
    
    for d in days:
        for t in teachings:
            # Assigning first and last slot of the day for each Teaching
            model.add(first_lecture_of_day[t.id_teaching, d] <= model.max(s * model.max(timetable_matrix[t2.id_teaching, s] for t2, corr in t.correlations.items()) for s in range(d*params.slot_per_day, (d+1)*params.slot_per_day) if s in slots))
            model.add(last_lecture_of_day[t.id_teaching, d] >= model.max(s * model.max(timetable_matrix[t2.id_teaching, s] for t2, corr in t.correlations.items()) for s in range(d*params.slot_per_day, (d+1)*params.slot_per_day) if s in slots))
    for d in days:
        for t in teachings:
            model.add(lectures_dispersion_of_day[t.id_teaching, d] == last_lecture_of_day[t.id_teaching, d] - first_lecture_of_day[t.id_teaching, d])

    # Add a target function that minimizes the dispersion
    model.minimize(model.sum(lectures_dispersion_of_day[t.id_teaching, d] for t in teachings for d in days))

'''
    Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
'''
def add_first_last_slot_correlation_limit(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for t1 in teachings:
        for t2, corr in t1.correlations.items():
            # Not applying this for the practice lectures and laboratories, since they are probably divided in groups. Need to verify that the timetable generated is good of if we need to apply this constraint to practices and labs as well
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2.id_teaching, s + (params.slot_per_day - 1)])
                for s in range(0, len(slots), 7) if s + (params.slot_per_day - 1) in slots) <= params.max_corr_first_last_slot)

'''
    Add the constraints for the Teachings to the model.
    This function calls the functions above one by one.
'''
def add_teachings_constraints(model, timetable_matrix, teachings, slots, days):
    # Note: moving the following constraints in a single "for teaching in teachings" will result in a different solution
    # We need to apply a constraint to all the teachings before applying the next constraint

    # Constraint: each Teaching must have exactly lect_slots Slots per week
    add_slots_per_week_teaching(model, timetable_matrix, teachings, slots)

    # Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
    add_daily_slots_constraints(model, timetable_matrix, teachings, slots, days)

    # Constraint: limiting the number of correlated lectures in a day
    # Constraint: a Teaching cannot overlap with the others, according to the correlations
    add_correlations_overlaps_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: I consider params.n_consecutive_slots consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
    add_consecutive_slots_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: the difference between the first and last lecture slot of the day should be minimized
    #add_first_last_lecture_of_day_limit(model, timetable_matrix, teachings, slots, days)

    # Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
    add_first_last_slot_correlation_limit(model, timetable_matrix, teachings, slots)
