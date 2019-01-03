#!/usr/bin/env python3

import sys
from itertools import combinations
from math import floor

# import numpy as np
from copy import copy

from InstanceSolution import *
from Instance import *
from utils import *

from Solver import *
import click

class BadDIMACSFormatError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def parse_dimacs(instance_file):
    instance = Instance()
    current = []
    read = 0
    for instance_line in instance_file:
        if instance.variables == -1 or instance.weights == []:
            if instance_line[0] == 'c':
                continue
            elif instance_line[0] == 'p':
                tokens = instance_line.split()
                if len(tokens) != 4:
                    raise BadDIMACSFormatError(f"Not enough parameters in problem line, found {len(tokens)}") 

                if tokens[1] != "cnf":
                    raise BadDIMACSFormatError(f"Not cnf format, is {tokens[0]}") 

                instance.variables = int(tokens[2])
                instance.clauses = int(tokens[3])
                continue
            elif instance_line[0] == 'w':
                tokens = instance_line.split()

                for token in tokens[1:]:
                    # print(token)
                    instance.weights.append(int(token))
                continue
            else:
                raise BadDIMACSFormatError(f"Invalid start of line char: {instance_line[0]}")


        end = False
        tokens = instance_line.split()
        for token in tokens:

            if token == "0":
                end = True
                break
            current.append(int(token))


        if end:
            instance.formula.append(current)
            current = []

            read += 1
            if read >= instance.clauses:
                break


    return instance
    

def parametrized(instance_file, algorithm):
    instances = {}
    solutions = {}
    relative_errors = []


    for instance_line in instance_file:
        instance = Instance(instance_line.rstrip('\n'))
        instances.update({instance.get_id(): instance})
    
    print("knapsack_id,algorithm,no_items,price,time_ms")


    # backpack_size = next(iter(solutions.values())).get_no_items()
    for id_inst, instance in instances.items():
        if algorithm == "genetic":
            method = Genetic()
            computed = method.solve(instance)
        time = measured_time[-1]['time']
        print(f'{id_inst},{algorithm},{instance.no_items},{computed.get_cost()},{time}')




def genetic(instance_file, xover_probability=0.4, mutation_probability=0.1, elitism_count=10,
            tournament_count=16, tournament_pool_size=2, generations=1000, constant=0.9):

    # print("xover_probability", xover_probability,
    #     "mutation_probability", mutation_probability, 
    #     "elitism_count", elitism_count,
    #     "tournament_count", tournament_count, 
    #     "tournament_pool_size", tournament_pool_size, 
    #     "generations", generations)

    instance = parse_dimacs(instance_file)



    method = Genetic(xover_probability=xover_probability,
                     mutation_probability=mutation_probability, 
                     elitism_count=elitism_count,
                     tournament_count=tournament_count, 
                     tournament_pool_size=tournament_pool_size, 
                     constant=constant,
                     generations=generations,
                     verbose=True)
    computed = method.solve(instance)

    print(computed)
    # print()
    # print(f'{id_inst},genetic,{instance.no_items},{computed.get_cost()}')
    # print ("ge:", computed)


    pass


@click.command()
@click.option('-m', '--mode', default="genetic", help='Output mode.   [default: genetic]')
@click.option('-a', '--algorithm', metavar='algorithm', help='Algorithm to chose when running parametrized mode.')
@click.option('-xp', '--xover_probability', default=0.4, type=float, help='xover_probability.')
@click.option('-mp', '--mutation_probability', default=0.1, type=float, help='mutation_probability.')
@click.option('-ec', '--elitism_count', default=10, type=int, help='elitism_count.')
@click.option('-tc', '--tournament_count', default=16, type=int, help='tournament_count.')
@click.option('-tps', '--tournament_pool_size', default=2, type=int, help='tournament_pool_size.')
@click.option('-ge', '--generations', default=1000, help='generations.')
@click.option('-c', '--constant', default=0.9, type=float, help='constant.')
@click.argument('instance_file', nargs=2)
# @click.argument('solution_file', nargs=-1)
def main(mode, algorithm, instance_file, xover_probability, mutation_probability, elitism_count,
            tournament_count, tournament_pool_size, generations, constant):
    if instance_file == None:
        print ("Instance file not supplied!", file=sys.stderr)
        sys.exit(1)


    # print("constant is", constant)
    # constant = 0.9
    instance_file_ptr = open(instance_file[1], "r")

    if mode == "parametrized":
        parametrized(instance_file_ptr, algorithm)

    if mode == "genetic":
        genetic(instance_file_ptr, 
                xover_probability=xover_probability,
                constant=constant,
                mutation_probability=mutation_probability, 
                elitism_count=elitism_count,
                tournament_count=tournament_count, 
                tournament_pool_size=tournament_pool_size, 
                generations=generations)


if __name__ == "__main__":
    main(sys.argv)
