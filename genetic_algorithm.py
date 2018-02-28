"""
genetic_algorithm.py: the base genetic_algorithm class.

"""

from genom_struct import GenomStruct
import numpy as np
import logging
import random


__author__ = "Mostafa Rafaie"
__license__ = "APLv2"


class GeneticAlgorithm:
    LOGGER_HANDLER_NAME = 'GA_LOG_HANDLER'

    # Cross Over Types
    SINGLE_POINT_CROSSOVER = 0
    TWO_POINT_CROSSOVER = 1
    CUT_SLICE_CROSSOVER = 2
    UNIFORM_CROSSOVER = 3

    CROSSOVER_FUNCTIONS=[do_crossover_single_point, do_crossover_two_point
                         do_crossover_cut_slice, do_crossover_uniform]

    def __init__(self, path, log_level=None):
        self.path = path
        self.gs = GenomStruct(path)
        self.logger = logging.getLogger(__name__)
        if log_level is not None:
            self.logger.setLevel(log_level)

    # Cross Over functions
    def do_crossover_single_point(self, genom1, genom2):
        c = random.randint(1, self.gs.size() - 2)
        return genom1[:c] + genom2[c:-1] + [0.0]

    def do_crossover_two_point(self, genom1, genom2):
        if self.gs.size() <= 3:
            return genom1[1] + genom2[2] + genom1[3] + [0.0]

        c1 = random.randint(0, self.gs.size() - 2)
        c2 = random.randint(c1, self.gs.size() - 1)
        return genom1[:c1] + genom2[c1:c2] + genom1[c2:-1] + [0.0]

    def do_crossover_cut_slice(self, genom1, genom2):
        c1 = random.randrange(0, self.gs.size() - 1)
        c2 = random.randrange(0, self.gs.size() - 1)
        g = genom1[:c1] + genom1[0][c2:]
        g = g[:self.gs.size() - 1]
        if len(g) < self.gs.size():
            g += self.gs.random_genom()[len(g):]
        return g + [0.0]

    def do_crossover_uniform(self, genom1, genom2):
        g = []
        for i in range(self.gs.size()):
            if random.randint(0, 1) == 1:
                g.append(genom1[i])
            else:
                g.append(genom2[i])

        return g + [0.0]

    def do_crossover(self, type, genom1, genom2):
        return self.CROSSOVER_FUNCTIONS[type](genom1, genom2)

    # Run the GA Algorithem
    def init_generation(self, init_population_size):
        self.logger.info('init_generation is started running')

        p = []
        counter = 0
        while counter < init_population_size:
            d = self.gs.random_genom() + [0.0]
            if d not in p:
                p.append(d)
                counter += 1

        population = np.array(p)

        self.logger.info('initialize the genration with the size of {}'.
                         format(len(population)))

        return population

    def init_ga(self, init_population_size, path=None):
        if path is not None:
            self.gs = GenomStruct(path)

        return self.init_generation(init_population_size)

    def calc_fitness(self, population, fitness, cuncurrency):
        pass

    def check_stop_condition(self, population, num_iteratitions, iteratition):
        pass

    def choose_best_population(self, population, population_size):
        pass

    def gen_next_generation(self, population_size, mutation_rate,
                            crossover_type, cuncurrency, fitness):
        pass

    def run(self, fitness, cuncurrency, init_population_size, population_size,
            mutation_rate, num_iteratitions, crossover_type, path=None):

        iteratition = 0
        population = self.init_ga(init_population_size, path)
        self.calc_fitness(population, fitness, cuncurrency)

        population = self.choose_best_population(population,
                                                 population_size)

        while self.check_stop_condition(population, num_iteratitions,
                                        iteratition):

            population = self.gen_next_generation(population_size,
                                                  mutation_rate,
                                                  crossover_type,
                                                  cuncurrency,
                                                  fitness)

            population = self.choose_best_population(population,
                                                     population_size)
        return population
