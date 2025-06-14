from Utils.Parameters import Parameters

'''Slots. I ask the user if they want to allocate lectures on Saturday or not. If yes, I need to know how many slots are available on Saturday (min. 0, max 7)'''
def get_slots_per_week(params):
    #Getting the program parameters

    print("Do you want to enable lectures on Saturday? (y/n): ")
    params.enable_saturday = input().lower() == "y"
    if params.enable_saturday:
        # Saturday enabled
        while True:
            print("How many Slots are available on Saturday? Min. 0 (no lectures on Saturday), max. 7): ")
            params.saturday_slots = int(input())

            # Validate the input
            if params.saturday_slots < 0 or params.saturday_slots > 7:
                print("The number of slots must be between 0 and 7.")
            else:
                if params.saturday_slots == 0:
                    params.set_saturday_enabled(False)

                # Set the number of Slot per week
                slots = range(5 * params.slot_per_day + params.saturday_slots)

                break
    else:
        # Set the number of Slot per week
        slots = range(5 * params.slot_per_day)

    return slots