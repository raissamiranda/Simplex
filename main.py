import numpy as np

# The tableau method for simplex 
class Tableau:
    def __init__(self):
        self.c = []                     # Objective function
        self.A = []                     # Restrictions
        self.b = []                     # Restrictions
        self.optimal_solution = 0       # Maximum optimal value
        self.base_columns = []          # Bases index
        self.dimension = (0,0)          # A's dimension
        self.identification = ''        # Optimal, unbounded or impossible

