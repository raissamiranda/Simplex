import numpy as np


# The tableau method for simplex 
class Tableau:
    def __init__(self):
        self.c = []                     # Objective function
        self.A = []                     # Constraints
        self.b = []                     # Constraints
        self.optimal_solution = 0       # Maximum optimal value
        self.base_columns = []          # Bases index
        self.dimension = (0,0)          # A's dimension
        self.identification = ''        # Optimal, unbounded or impossible


# Converting an LP into canonical form
def canonical_form(self):
    # Make all the basic variables pivots values equal to 1 and the other variables 0 (includind c inputs)
    for i in range(self.dimensions[0]):                      # For each basic variable
        if(self.A[i][self.base_columns[i]] != 0):            # Pivot is not null
            aux = self.A[i][self.base_columns[i]].copy()     # Value that annuls the variable when divided
            self.A[i,:] /= aux                               # Make pivot value equals to 1
            self.b[i] /= aux                                 # Vector b is also divided
        for j in range(self.dimension[0]):                   # For each line
            if (i != j):                                     # It's not the basic variable line
                aux = self.A[j][self.base_columns[i]].copy() # Value that should be null
                self.A[j,:] -= aux * self.A[i,:]             # Subtract all the line
                self.b[j] -= aux * self.b[i]                 # Vector b is also subtracted
        aux = self.c[self.base_columns[i]]                   # c input must also be null
        self.c -= aux * self.A[i,:]                          # Substract all the vector c
        self.optimal_solution -= aux * self.b[i]             # Substract the optimal value with respect to vector b
    vfunc = np.vectorize(round_zero)                         # Applies the function in parameter in all the vector's input
    self.A = vfunc(self.A)                                   # (set very low values to zero)
    self.b = vfunc(self.b)
    self.c = vfunc(self.c)
    self.optimal_solution = vfunc(self.optimal_solution)