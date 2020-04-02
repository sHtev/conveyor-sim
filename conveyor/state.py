import random
import string


def get_new_items(component_types, number_of_items):
    # Components are represented by upper case letters
    choices = [' '] + list(string.ascii_uppercase[:component_types])
    return random.choices(choices, k=number_of_items)


def initialise_state(belt_length, component_types, is_empty):
    upper = [('v', [], 0)] * belt_length
    lower = [('^', [], 0)] * belt_length

    if is_empty:
        belt = [' '] * belt_length
    else:
        belt = get_new_items(component_types, belt_length)

    return upper, lower, belt
