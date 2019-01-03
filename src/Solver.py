from InstanceSolution import InstanceSolution
from utils import *
import random
import copy
import math

class Solver(object):
    """Generic solver class"""
    def __init__(self):
        super(Solver, self).__init__()

    def solve(self):
        pass
        



class Genetic(Solver):
    """Solver class for Generic algorithm"""
    def __init__(self, xover_probability=0.4, mutation_probability=0.1, elitism_count=10,
                tournament_count=16, tournament_pool_size=2, generations=1000, verbose=False, constant=0.9):
        super(Genetic, self).__init__()
        self.population_size = 100
        # self.items = []
        # self.capacity = 0

        self.constant = constant
        self.xover_probability = xover_probability
        self.genome_size = 0
        self.mutation_probability = mutation_probability
        self.elitism_count = elitism_count
        self.tournament_count = tournament_count
        self.tournament_pool_size = tournament_pool_size
        self.generations = generations
        self.verbose = verbose


        self.use_constraint = False

    def save_best(self, best):
        for index, item in enumerate(best):
            if item == True:
                self.items[index]['entered'] = True

    def get_cost(self):
        return sum([x['price'] for x in self.items if x['entered']])
        

    def knap_to_bits(self, items):
        prices = [i['price'] for i in items]
        weights = [i['weight'] for i in items]
        return prices, weights
        
    def count_satisfied_formulas(self, individual):
        # print("genom:_____")
        # for i in individual:
            # print(i, sep=" ")
        # print("individual:", individual)
        acc = 0

        for clause in self.formula:
            # print(clause)
            # print("-----")
            for var in clause:
                index = abs(var) - 1
                if (var <0 and individual[index] == 1) or (var >0 and individual[index] == 0):
                    # print("Mam te!")
                    # print(var)
                    # print(index)
                    acc += 1
                    break

                # print("------")


        # print("------")

        return acc
        pass

    def sum_valid_weights(self, individual):
        sum_val = 0
        for i, value in enumerate(individual):
            if value == 1:
                sum_val += self.weights[i]

        return sum_val

        pass

    def fitness_fn(self, individual):

        satisfied = self.count_satisfied_formulas(individual)
        sum_weights = self.sum_valid_weights(individual)

        # k = 0.9

        # print("Satisfied",satisfied)
        # print("sum",sum_weights)
        # price = 0
        # weight = 0
        # print(individual)

        fitness = 10000.0 * math.log(self.constant * math.exp(satisfied / self.clauses) + (1.0 - self.constant) * math.exp(sum_weights / self.maximum))


        # print("fitnessko", fitness)


        return fitness
        # for index, item in enumerate(population):
        #     if item == True:
        #         price = price + self.items[index]['price']
        #         weight = weight + self.items[index]['weight']
        # if weight <= self.capacity:
        #     return price
        # else:
        #     return 0

    def constraint_fn(self, individual):
        satisfied = self.count_satisfied_formulas(individual)

        if satisfied == self.clauses:
            return True
        return False

        # weight = 0
        # for index, item in enumerate(population):
        #     if item == True:
        #         weight = weight + self.items[index]['weight']

        # return weight <= self.capacity
        pass

    def create_individual(self, indiv_size):
        individual = [ random.choice([1, 0]) for i in range(0, indiv_size)]
        return individual

    def random_individual(self, population):
        pop_range = len(population)
        return population[random.randint(0, pop_range-1)]

    def create_population(self, population_size, indiv_size):
        population = [self.create_individual(indiv_size) for i in range(0, population_size)]
        return population

    def sort_population(self, population):
        """ Sort population acording to fitness function """
        sorted_pop = sorted(population, key=lambda x: self.fitness_fn(x), reverse=True)
        return sorted_pop

    def tournament(self, population, tournament_count, tournament_pool_size):

        new_population = []
        population_size = len(population)

        # Number of tournaments
        for _ in range(tournament_count):
            pool = []

            # Select individuals of tournament
            for _ in range(tournament_pool_size):
                pool.append(self.random_individual(population))
                
            sorted_pop = self.sort_population(pool)

            # Select the best from the tournament
            new_population.append(self.sort_population(pool)[0])
            
        return new_population
        
    def crossover_single(self, in1, in2):
        size = len(in1)
        child = copy.deepcopy(in1)
        midpoint = random.randint(0, size)

        for i in range(0, size):
            if i < midpoint:
                child[i] = in1[i]
            else:
                child[i] = in2[i]
        return child


    def mutator_random_inverse(self, child, mutation_probability):
        for index, item in enumerate(child):
            if odds_are(mutation_probability):
                if item == True:
                    child[index] = 0
                else:
                    child[index] = 1
        return child

    def simulate(self):

        # Create initial population
        population = self.create_population(self.population_size, self.genome_size )

        if self.verbose:
            print("generation,best_combination")
            best = 0

        # print('lets run generations')
        # Run n generations
        for generation in range(0, self.generations):
            # print("gen no ", generation)
            sorted_population = self.sort_population(population)

            new_best = self.fitness_fn(sorted_population[0])

            if self.verbose:
                # if new_best > best:
                #     print(generation, new_best, sep=",")
                #     best = new_best
                print(generation, new_best, sep=",")


            # Selection
            new_population = self.tournament(population, self.tournament_count, self.tournament_pool_size )


            # Elitsm
            del sorted_population[self.elitism_count:]


            new_population.extend(sorted_population)
            sorted_population = self.sort_population(new_population)


            # Fill population with new children
            while len(new_population) != self.population_size:
                # print("adding new individual", len(new_population), self.population_size)
                child = []
                # Crossover
                if odds_are(self.xover_probability):

                    in1 = self.random_individual(new_population)
                    in2 = self.random_individual(new_population)

                    child = self.crossover_single(in1, in2)

                else:
                    # Just pick random individual
                    child = copy.deepcopy(self.random_individual(population))

                # Mutation
                child = self.mutator_random_inverse(child, self.mutation_probability)

                # Check if mutated/crossed individual is valid
                if not self.use_constraint or self.constraint_fn(child):
                    new_population.append(child)

            population = new_population

        sorted_population = self.sort_population(population)

        return sorted_population[0]

    def solve(self, instance):

        self.clauses =  instance.clauses

        self.formula = instance.formula

        self.maximum = sum(instance.weights)

        # print("max:", self.maximum)

        self.genome_size = instance.variables
        self.weights = instance.weights
        # self.items = instance.items
        # self.capacity = instance.capacity
            
        # self.


        best = self.simulate()
        best_cost = self.fitness_fn(best)

        # self.save_best(best)
        return InstanceSolution(
            best_cost=best_cost,
            satisfied=self.count_satisfied_formulas(best),
            variables=instance.variables,
            clauses=instance.clauses,
            weight=self.sum_valid_weights(best),
            best_combination=best)

