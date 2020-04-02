import random

from .state import get_new_items


def get_action_for_worker(worker, belt_item, component_types):
    # If assembling, keep assembling
    if worker[0] == '*':
        return '*'
    # If free space on belt place product
    if belt_item == ' ' and worker[0] == 'P':
        return 'P'
    # If no space, keep product and do nothing
    if worker[0] == 'P':
        return '-'
    # If item needed on belt, pick it up
    if belt_item not in [' ', 'P'] and belt_item not in worker[1]:
        return belt_item
    # If have all tems, start working
    if len(worker[1]) == component_types:
        return '*'
    # Otherwise wait
    else:
        return '-'


def resolve_action_conflicts(actions):
    # Decide worker order
    first_choice = random.randint(0, 1)
    second_choice = 1-first_choice

    # Block worker who goes second if first worker puts or takes
    # i.e. isn't assembling or waiting
    if actions[first_choice] not in ['*', '-']:
        actions[second_choice] = '-'

    return actions


def generate_actions(belt, upper, lower, component_types):
    upper_actions = []
    lower_actions = []

    for ind, space in enumerate(belt):
        # Get best possible actions for all workers
        upper_action = get_action_for_worker(upper[ind], space, component_types)
        lower_action = get_action_for_worker(lower[ind], space, component_types)

        # Resolve conflicts
        resolved_actions = resolve_action_conflicts([upper_action, lower_action])
        upper_actions.append(resolved_actions[0])
        lower_actions.append(resolved_actions[1])

    return [upper_actions, lower_actions]


def perform_action_for_worker(worker, action, item, assemble_time, default_state):
    # Doing nothing, nothing changes
    if action == '-':
        return worker, item
    # Start new assembly
    if action == '*' and worker[2] < assemble_time:
        return ('*', ['*'], worker[2] + 1), item
    # Finish assembly, worker has product
    if action == '*':
        return ('P', ['P'], 0), item
    # Put product on belt
    if action == 'P' and item == ' ':
        return (default_state, [], 0), 'P'
    # Take product from belt
    return (item, worker[1] + [item], 0), ' '


def perform_step(actions, belt, upper, lower, assemble_time, component_types):
    # Next item for belt
    new_belt = get_new_items(component_types, 1)
    uppers = []
    lowers = []

    # Look at each belt position
    for ind, item in enumerate(belt):
        # Take or place
        upper_worker, item = perform_action_for_worker(upper[ind], actions[0][ind], item, assemble_time, 'v')
        lower_worker, item = perform_action_for_worker(lower[ind], actions[1][ind], item, assemble_time, '^')

        # Update worker state
        uppers.append(upper_worker)
        lowers.append(lower_worker)

        # Items go to next belt position for next iteration
        new_belt.append(item)

    # Output is last item
    output = new_belt[-1]

    return uppers, lowers, new_belt[:-1], output
