from collections import defaultdict

import click

from .actions import generate_actions, perform_step
from .state import initialise_state


@click.command()
@click.option('-a', '--assemble-time', 'assemble_time', default=3,
              help='Number of steps for a worker to assemble a component.')
@click.option('-b', '--belt', default=3, help='Length of conveyor belt.')
@click.option('-e', '--empty', is_flag=True, help='Start with an empty conveyor belt.')
@click.option('-c', '--components', default=2, help='Number of product components.')
@click.option('-i', '--iterations', default=1,  help='Simulation interations to run.')
@click.option('-s', '--steps', default=100, help='Number of steps to simulate.')
@click.option('-v', '--visuals/--no-visuals', 'visualise', help='Show graphical visualisation of simulation.')
def simulate(assemble_time, belt, components, empty, iterations, steps, visualise):
    upper, lower, items = initialise_state(belt, components, empty)

    products = 0
    waste = defaultdict(lambda: 0)

    for i in range(steps):
        if visualise:
            # update graphics
            # temp for test
            print([worker[0] for worker in upper])
            print(items)
            print([worker[0] for worker in lower])
            input()

        # Get actions for workers
        actions = generate_actions(items, upper, lower, components)
        # Update state with actions
        upper, lower, items, output = perform_step(actions, items, upper, lower, assemble_time, components)

        # Update output stats
        if output == 'P':
            products += 1
        elif output != ' ':
            waste[output] += 1

    if not waste:
        waste = 0
    else:
        waste = dict(waste)

    print(f'Total products produced: {products}, total components wasted: {waste}')
