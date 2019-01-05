class InstanceSolution(object):
    def __init__(self, **kwargs):
        super(InstanceSolution, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


    def __eq__(self, other):
        return (self.no_items, self.best_cost, self.best_combination) == (other.no_items, other.best_cost,other.best_combination)

    def __repr__(self):
        return "price,variables,clausules,satisfied,weight,valid\n{},{},{},{},{},{}".format(str(self.best_cost), str(self.variables), str(self.clauses), str(self.satisfied), str(self.weight), str(self.valid))
        # return "{} {} {}".format(str(self.no_items), str(self.best_cost), str(self.best_combination))

    def get_id(self):
        return self.id

    def get_no_items(self):
        return self.no_items

    def get_cost(self):
        return self.best_cost

    def get_solution_line(self):
        return self.no_items, self.best_cost, self.best_combination
