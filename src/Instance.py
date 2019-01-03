from utils import *

from InstanceSolution import InstanceSolution



class Instance(object):

    def __init__(self, variables, clauses, formula):
        self.variables = variables
        self.clauses = clauses
        self.formula = formula
        self.weights = weights

        self.maximum = 0

        pass

    def __init__(self):
        self.variables = -1
        self.weights = []
        self.clauses = 0
        self.formula = []

        self.maximum = 0
        
        pass
        
    def __repr__(self):
        return "{} {} W:{} {}".format(str(self.variables), str(self.clauses), str(self.weights), str(self.formula))

    def get_items(self):
        return self.items

    def get_capacity(self):
        return self.capacity


    def get_id(self):
        return self.id

