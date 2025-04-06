import math

from Utils.Parameters import Parameters

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_teaching(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for teaching in teachings:
        # lect_hours/params.n_weeks_in_semester gives the number of hours per week for a Teaching. Dividing this number by 1.5 returns the number of Slots in a week
        model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching, s] for s in slots) == teaching.lect_slots)

        '''Practice Slots'''
        if teaching.practice_slots != 0:
            # Considering the Groups for Practice Slots
            for i in range(1, teaching.n_practice_groups + 1):
                model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] for s in slots) == teaching.practice_slots)
        # TODO: Needs to be implemented and tested with a Pro version of CPLEX
        '''Lab Slots'''
        '''
        if teaching.lab_slots != 0:
            # Considering the Groups for Lab Slots
            for i in range(1, teaching.n_lab_groups):
                model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching + f"_lab_group{i}", s] for s in slots) == teaching.lab_slots)
        '''

'''
    Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
'''
def add_daily_slots_constraints(model, timetable_matrix, teachings, slots, days):
    # Note: this constraint should only be applied to Lecture Slots and not Laboratory Slots

    params = Parameters()

    # Variable that counts how many hours a teaching has in a day
    n_slots_in_day_teaching = {(teaching.id_teaching, d): model.integer_var(0, 2, name=f"y_{teaching.id_teaching}_{d}")
                               for teaching in teachings for d in days}

    # double_slots_in_day = 1 if the Lecture/Practice/Lab has at least 2 Slots in that Day
    double_slots_in_day = {}
    for teaching in teachings:
        for d in days:
            double_slots_in_day[teaching.id_teaching, d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching}_{d}")

            '''Practice Slots'''
            if teaching.practice_slots != 0:
                for i in range(1, teaching.n_practice_groups + 1):
                        double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")

    for teaching in teachings:
        for d in days:
            # Counts how many hours the Teaching t has in Day d
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] == model.sum(
                timetable_matrix[teaching.id_teaching, s] for s in
                range(d * params.slot_per_day, (d + 1) * params.slot_per_day)))

            # Counting how many days have 2 or more Slots of the same lecture
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] >= 2*double_slots_in_day[teaching.id_teaching, d])

            # Assign max consecutive Slots for a lecture according to teaching.n_min_double_slots_lecture
            if teaching.n_min_double_slots_lecture > 2:
                max_consecutive_slots = teaching.n_min_double_slots_lecture
            else:
                max_consecutive_slots = 2

            # Add the constraint that a Teaching should have a maximum of max_consecutive_slots Slots in a day (only for Lectures and not for Laboratories)
            if teaching.n_min_single_slots_lecture > 0 or teaching.n_min_double_slots_lecture == 0:
                model.add(n_slots_in_day_teaching[teaching.id_teaching, d] <= max_consecutive_slots)
            else:
                # If a Teaching can not have at least 1 single slot lecture, then it should only have double Slots

                # Checking that the number of Slots of a Teaching is even, in order to allocate only double Slots
                if teaching.lect_slots % 2 == 0:
                    model.add(model.logical_or(n_slots_in_day_teaching[teaching.id_teaching, d] == 0, n_slots_in_day_teaching[teaching.id_teaching, d] == max_consecutive_slots))
                else:
                    model.add(n_slots_in_day_teaching[teaching.id_teaching, d] <= max_consecutive_slots)

            # If n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
            for s in range(len(slots) - 1):
                if math.floor(s / params.slot_per_day) == d and math.floor((s + 1) / params.slot_per_day) == d:
                    # I consider 2 consecutive Slots. Those Slots should either have no lectures for this Teaching (== 0) or they should have n_slots_in_day_teaching lectures, to be sure that those lectures are consecutive
                    model.add(model.logical_or(timetable_matrix[teaching.id_teaching, s] == 0, (timetable_matrix[teaching.id_teaching, s] + timetable_matrix[teaching.id_teaching, s + 1]) >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching, d])))

                    '''Practice Slots'''
                    # If teaching.n_min_double_slots_practice >= 1, then I impose that the Teaching must have at leat 2 consecutive practice hours
                    # I check that there are at least 2 Slots of practice (to be sure that I can have 2 consecutive Slots)
                    if teaching.practice_slots >= teaching.n_min_double_slots_practice+1 and teaching.practice_slots%2 == 0 and teaching.n_min_double_slots_practice >= 1 and teaching.n_min_single_slots_practice == 0:
                        for i in range(1, teaching.n_practice_groups + 1):
                            model.add(model.logical_or(timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] == 0, (timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] + timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1]) == 2))

        # Constraint: if the Teaching has to have at least 1 double Slot, then I impose that condition
        if teaching.n_min_double_slots_lecture >= 1 and teaching.lect_slots >= teaching.n_min_double_slots_practice+1:
            model.add(model.sum(double_slots_in_day[teaching.id_teaching, d] for d in days) >= 1)

        '''Practice Slots'''
        if teaching.practice_slots != 0 and teaching.n_min_double_slots_practice >= 1 and teaching.practice_slots >= 2:
            for i in range(1, teaching.n_practice_groups + 1):
                model.add(model.sum(double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d] for d in days) >= 1)

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
                if t1.id_teaching < t2.id_teaching:
                    model.add(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2.id_teaching, s] <= 1)

                '''Practice Slots'''
                # Adding the constraint to the Practice Slots
                if t1.practice_slots != 0:
                    for i in range(1, t1.n_practice_groups + 1):
                        model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[t2.id_teaching, s] <= 1)
                        # Note: the same Groups of Practice Lectures can not overlap (e.g. Group1 of TeachingA can not overlap with Group1 of TeachingB, but Group1 of TeachingA CAN overlap with Group1 of TeachingB
                        if t2.practice_slots != 0 and i <= t2.n_practice_groups and t1.id_teaching < t2.id_teaching:
                            model.add(timetable_matrix[t1.id_teaching + f"_practice_group{i}", s] + timetable_matrix[t2.id_teaching + f"_practice_group{i}", s] <= 1)

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

    # TODO: cannot be tested with the free version of CPLEX due to its limitations, we need the server
    # Not applying this for the practice lectures and laboratories, since they are probably divided in groups. Need to verify that the timetable generated is good of if we need to apply this constraint to practices and labs as well
    '''
    for d in days:
        for t in teachings:
            # Assigning first and last slot of the day for each Teaching
            model.add(first_lecture_of_day[t.id_teaching, d] <= model.max(s * model.max(timetable_matrix[t_id, s] for t_id, corr in t.correlations.items()) for s in range(d*params.slot_per_day, (d+1)*params.slot_per_day) if s in slots))
            model.add(last_lecture_of_day[t.id_teaching, d] >= model.max(s * model.max(timetable_matrix[t_id, s] for t_id, corr in t.correlations.items()) for s in range(d*params.slot_per_day, (d+1)*params.slot_per_day) if s in slots))
    for d in days:
        for t in teachings:
            model.add(lectures_dispersion_of_day[t.id_teaching, d] == last_lecture_of_day[t.id_teaching, d] - first_lecture_of_day[t.id_teaching, d])

    # Add a target function that minimizes the dispersion
    model.minimize(model.sum(lectures_dispersion_of_day[t.id_teaching, d] for t in teachings for d in days))
    '''

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

    # Constraint: each Teaching must have exactly (lect_slots/params.n_weeks_in_semester) / params.hours_in_slot Slots per week
    add_slots_per_week_teaching(model, timetable_matrix, teachings, slots)

    # Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
    # Constraint: each Teaching must appear in a maximum of params.max_days_teaching days
    add_daily_slots_constraints(model, timetable_matrix, teachings, slots, days)

    # Constraint: limiting the number of correlated lectures in a day
    # Constraint: a Teaching cannot overlap with the others, according to the correlations
    add_correlations_overlaps_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: I consider params.n_consecutive_slots consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
    add_consecutive_slots_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: the difference between the first and last lecture slot of the day should be minimized
    add_first_last_lecture_of_day_limit(model, timetable_matrix, teachings, slots, days)

    # Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
    add_first_last_slot_correlation_limit(model, timetable_matrix, teachings, slots)