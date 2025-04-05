import math

from Utils.Parameters import Parameters

'''
    Add the constraint about the number of Slots that each Teaching should have in a week
'''
def add_slots_per_week_teaching(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for teaching in teachings:
        # lect_hours/params.n_weeks_in_semester gives the number of hours per week for a Teaching. Dividing this number by 1.5 returns the number of Slots in a week
        model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching, s] for s in slots) == math.ceil((teaching.lect_hours / params.n_weeks_in_semester) / params.hours_in_slot))

        # Adding constraint for Practice Lectures and Laboratories
        # TODO: Needs to be implemented and tested with a Pro version of CPLEX

        if teaching.practice_hours != 0:
            model.add_constraint(model.sum(timetable_matrix[teaching.id_teaching + '_practice', s] for s in slots) == math.ceil((teaching.practice_hours / params.n_weeks_in_semester) / params.hours_in_slot))

'''
    Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
    Constraint: each Teaching must appear in a maximum of params.max_days_teaching days
'''
def add_daily_constraints(model, timetable_matrix, teachings, slots, days):
    # TODO: this constraint should only be applied to Lecture Slots and not Laboratory Slots
    # TODO: the maximum number of days is modeled as a hard constraint for testing purposes, but may be better as a soft constraint

    params = Parameters()

    # Variable that counts how many hours a teaching has in a day
    n_slots_in_day_teaching = {(t.id_teaching, d): model.integer_var(0, 2, name=f"y_{t.id_teaching}_{d}")
                               for t in teachings for d in days}
    # Variable that is 1 if the Teaching t appears in Day d, 0 otherwise
    n_days_teaching = {(t.id_teaching, d): model.binary_var(name=f"y_{t.id_teaching}_{d}")
                       for t in teachings for d in days}

    for teaching in teachings:
        for d in days:
            # Counts how many hours the Teaching t has in Day d
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] == model.sum(
                timetable_matrix[teaching.id_teaching, s] for s in
                range(d * params.slot_per_day, (d + 1) * params.slot_per_day)))
            # Counts in how many days the Teaching t appears
            model.add(n_days_teaching[teaching.id_teaching, d] >= n_slots_in_day_teaching[teaching.id_teaching, d] / 2)
            model.add(n_days_teaching[teaching.id_teaching, d] <= n_slots_in_day_teaching[teaching.id_teaching, d])

            # Add the constraint that a Teaching should have a maximum of params.max_consecutive_slots_teaching Slots in a day (only for Lectures and not for Laboratories)
            model.add(n_slots_in_day_teaching[teaching.id_teaching, d] <= params.max_consecutive_slots_teaching)
            # Add the constraint that a Teaching must appear in a maximum of params.max_days_teaching
            # model.add(model.sum(n_days_teaching[t.id_teaching, day] for day in days) <= params.max_days_teaching)

            # If n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
            for s in range(len(slots) - 1):
                if math.floor(s / params.slot_per_day) == d and math.floor((s + 1) / params.slot_per_day) == d:
                    model.add(model.logical_or(timetable_matrix[teaching.id_teaching, s] == 0, (timetable_matrix[teaching.id_teaching, s] + timetable_matrix[teaching.id_teaching, s + 1]) >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching, d])))

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
            model.add_constraint(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2_id, s + i])
                for i in range(1, params.slot_per_day - (s % params.slot_per_day)) if s + i in slots
                for t2_id, corr in t1.correlations.items()) <= params.max_corr_in_day)

            # Constraint: a Teaching cannot overlap with the others, according to the correlations
            for t2_id, corr in t1.correlations.items():
                # I need this if in order to not impose the same constraint twice (e.g. one from 267072 to 267158 and the other from 267158 to 267072)
                if t1.id_teaching < t2_id:
                    model.add_constraint(timetable_matrix[t1.id_teaching, s] + timetable_matrix[t2_id, s] <= 1)

'''
    Constraint: I consider params.n_consecutive_slots consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
'''
def add_consecutive_slots_constraint(model, timetable_matrix, teachings, slots):
    params = Parameters()

    for s in range(len(slots) - (params.n_consecutive_slots - 1)):
        for t1 in teachings:
            correlations_in_slots = model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2_id, s + i])
                for i in range(1, params.n_consecutive_slots)
                for t2_id, corr in t1.correlations.items())

            model.add(1 == model.logical_or(correlations_in_slots == 0, correlations_in_slots >= params.min_corr_in_slots))

'''
    Constraint: the difference between the first and last lecture slot of the day should be minimized
'''
def add_first_last_lecture_of_day_limit(model, timetable_matrix, teachings, slots, days):
    params = Parameters()

    # Variables that save the first and last lecture Slots, for each Day and Teaching
    first_lecture_of_day = {
        (t.id_teaching, d): model.integer_var(0, len(slots) - 1, name=f"first_lecture_{t.id_teaching}_{d}") for t in
        teachings for d in days}
    last_lecture_of_day = {
        (t.id_teaching, d): model.integer_var(0, len(slots) - 1, name=f"last_lecture_{t.id_teaching}_{d}") for t in
        teachings for d in days}
    # Variable that saves the difference between the first and last lecture Slot, for each Day and Teaching
    lectures_dispersion_of_day = {(t.id_teaching, d): model.integer_var(0, params.slot_per_day - 1, name=f"lecture_dispersion_{t.id_teaching}_{d}") for t in teachings for d in days}

    # TODO: cannot be tested with the free version of CPLEX due to its limitations, we need the server
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
        for t2_id, corr in t1.correlations.items():
            model.add(model.sum(
                corr * (timetable_matrix[t1.id_teaching, s] * timetable_matrix[t2_id, s + (params.slot_per_day - 1)])
                for s in range(0, len(slots), 7) if s + (params.slot_per_day - 1) in slots) <= params.max_corr_first_last_slot)

'''
    Add the constraints for the Teachings to the model
'''
def add_teachings_constraints(model, timetable_matrix, teachings, slots, days):
    params = Parameters()

    # Note: moving the following constraints in a single "for teaching in teachings" will result in a different solution
    # We need to apply a constraint to all the teachings before applying the next constraint

    # Constraint: each Teaching must have exactly (lect_hours/params.n_weeks_in_semester) / params.hours_in_slot Slots per week
    add_slots_per_week_teaching(model, timetable_matrix, teachings, slots)

    # Constraint: each Teaching must have 0..2 Slots per day and, if it has 2 Slots, they should be consecutive
    # Constraint: each Teaching must appear in a maximum of params.max_days_teaching days
    add_daily_constraints(model, timetable_matrix, teachings, slots, days)

    # Constraint: limiting the number of correlated lectures in a day
    # Constraint: a Teaching cannot overlap with the others, according to the correlations
    add_correlations_overlaps_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: I consider params.n_consecutive_slots consecutive slots. I impose a minimum number of correlated lectures in those slots, in order to limit the number of empty slots in a day
    add_consecutive_slots_constraint(model, timetable_matrix, teachings, slots)

    # Constraint: the difference between the first and last lecture slot of the day should be minimized
    add_first_last_lecture_of_day_limit(model, timetable_matrix, teachings, slots, days)

    # Constraint: the correlation between teachings in the first and last slot of the day should be <= params.max_corr_first_last_slot, in order to avoid that the majority of students starts at 8:30 and finishes at 19:00
    add_first_last_slot_correlation_limit(model, timetable_matrix, teachings, slots)