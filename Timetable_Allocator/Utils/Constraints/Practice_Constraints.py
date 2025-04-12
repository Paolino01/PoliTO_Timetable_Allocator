'''
    In this file there are the functions needed to add the Constraints about Practice Slots to the model
'''
from Utils.Components.Teaching import Teaching
from Utils.Parameters import Parameters


def add_slots_per_week_practice(model, timetable_matrix, teaching, slots):
    if teaching.practice_slots != 0:
        # Considering the Groups for Practice Slots
        for i in range(1, teaching.n_practice_groups + 1):
            model.add_constraint(
                model.sum(timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] for s in slots)
                == teaching.practice_slots
            )

'''
    Add the constraint that if n_slots_in_day_teaching[t.id_teaching, d] >= 2, the Slots should be consecutive
'''
def add_double_slots_constraint_practice(model, timetable_matrix, teaching: Teaching, s, d, n_slots_in_day_teaching):
    for i in range(1, teaching.n_practice_groups + 1):
        # If teaching.n_min_double_slots_practice >= 1, then I impose that the Teaching must have at leat 2 consecutive practice hours
        # I check that there are at least 2 Slots of practice (to be sure that I can have 2 consecutive Slots)
        if teaching.practice_slots >= teaching.n_min_double_slots_practice + 1 and teaching.practice_slots % 2 == 0 and teaching.n_min_double_slots_practice >= 1 and teaching.n_min_single_slots_practice == 0:
            model.add(
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] == 0,
                    (
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] +
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1]
                    )
                    == 2
                )
            )
        # If I don't have any constraint about the minimum number of double Slots, I just impose that if there are any double Slots the are consecutive
        else:
            if teaching.practice_slots > 0:
                model.logical_or(
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] == 0,
                    (
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s] +
                        timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s + 1]
                    )
                    >= model.min(2, n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d])
                )

'''
    Constraint: if the Practice Lecture has to have at least 1 double Slot, then I impose that condition
'''
def add_min_double_slots_contraint_practice(model, teaching, days, double_slots_in_day):
    if teaching.practice_slots != 0 and teaching.n_min_double_slots_practice >= 1 and teaching.practice_slots >= 2:
        for i in range(1, teaching.n_practice_groups + 1):
            model.add(
                model.sum(double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d] for d in days) >= 1)

'''
    Defines the variables n_slots_in_day_teaching and double_slots_in_day which contain the number of Practice Slots in a day and days with double Practice Slots
'''
def define_double_slots_in_day_practice(model, teaching, d, n_slots_in_day_teaching, double_slots_in_day):
    params = Parameters()

    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] = model.integer_var(0, params.max_consecutive_slots_teaching, name=f"y_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")
            double_slots_in_day[teaching.id_teaching + f"_practice_group{i}", d] = model.binary_var(name=f"double_slots_in_day_{teaching.id_teaching + '_practice_group' + str(i)}_{d}")

'''
    Adds the number of Practice Slots in a day to the variable n_slots_in_day_teaching
'''
def count_double_slots_in_day_practice(model, timetable_matrix, teaching, d, n_slots_in_day_teaching):
    params = Parameters()

    if teaching.practice_slots != 0:
        for i in range(1, teaching.n_practice_groups + 1):
            model.add(n_slots_in_day_teaching[teaching.id_teaching + f"_practice_group{i}", d] ==
                model.sum
                (
                    timetable_matrix[teaching.id_teaching + f"_practice_group{i}", s]
                    for s in range(d * params.slot_per_day, (d + 1) * params.slot_per_day)
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