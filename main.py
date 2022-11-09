import numpy as np
import copy


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


# Set very low values to zero
def rounding_to_zero(value):
    if (abs(value) < 1e-4):
        value = 0.0
    return value


# Converting an LP into canonical form
def canonical_form(self):
    # Make all the basic variables pivots values equal to 1 and the other variables 0 (includind c inputs)
    for i in range(self.dimension[0]):                               # For each basic variable
        if(self.A[i][self.base_columns[i]] != 0):                    # Pivot is not null
            aux = copy.deepcopy(self.A[i][self.base_columns[i]])     # Value that annuls the variable when divided
            self.A[i,:] /= aux                                       # Make pivot value equals to 1
            self.b[i] /= aux                                         # Vector b is also divided
        for j in range(self.dimension[0]):                           # For each line
            if (i != j):                                             # It's not the basic variable line
                aux = copy.deepcopy(self.A[j][self.base_columns[i]]) # Value that should be null
                self.A[j,:] -= aux * self.A[i,:]                     # Subtract all the line
                self.b[j] -= aux * self.b[i]                         # Vector b is also subtracted
        aux = self.c[self.base_columns[i]]                           # c input must also be null
        self.c -= aux * self.A[i,:]                                  # Substract all the vector c
        self.optimal_solution -= aux * self.b[i]                     # Substract the optimal value with respect to vector b
    vfunc = np.vectorize(rounding_to_zero)                           # Applies the function in parameter in all the vector's input
    self.A = vfunc(self.A)                                           # (set very low values to zero)
    self.b = vfunc(self.b)
    self.c = vfunc(self.c)
    self.optimal_solution = vfunc(self.optimal_solution)


# Following Bland's rule, find the pivot element in the correct column and line and check if it's an unbounded LP
def find_pivot(self):
    for i in range(self.dimension[1]):                              # For each column
        is_unbounded = False
        pivot_column = i                                            # Pivot column index
        pivot_line = 0                                              # Pivot row index
        if(self.c[i] < 0):                                          # Negative input in c found
            c_aux = copy.deepcopy(self.c)
            c_aux = np.delete(c_aux, [i])
            # Checking unbounded PL
            if(np.all(self.A[:, i] <= 0) and (np.all(c_aux >= 0) or i < self.dimensions[1] - self.dimensions[0])):
                is_unbounded = True
                break                                               # Computing optimal value is impossible
            if(self.c[i] < 0):
                min_value = 100                                     # Maximum value for all the constraint variables
                for j in range(self.dimension[0]):                  # Find the minimum value for all the lines in this column
                    if(self.A[j][i] != 0):
                        candidate_value = self.b[j] / self.A[j][i]  # The minimum value is the new pivot
                        if(candidate_value < min_value and candidate_value >= 0 and self.A[j][i] > 0):
                            min_value = candidate_value             # The current minimum value
                            pivot_line = j                          # The current pivot row index
                break                                               # New pivot is found
    return pivot_column, pivot_line, is_unbounded




# Tests
c = [1,2,3,4]
A = [[2,5,3,4],
     [3,2,4,9],
     [4,3,2,5]]
b = [10,15,20,25]

teste = Tableau()
teste.c = np.array(c, dtype = float)
teste.A = np.array(A, dtype = float)
teste.b = np.array(b, dtype = float)
teste.base_columns = [1,2,3]
teste.dimension = (3,4)

canonical_form(teste)
print(teste.A)
print(teste.b)
print(teste.c)



