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
        self.certificate = []           # Identification certificate
        self.vero = []                  # Auxiliar matrix for finding certificate


# For testing
def print_tableau(self):
    print('A = ')
    print(self.A)
    print('b = ', self.b)
    print('c = ', self.c)
    print('optimal solution = ', self.optimal_solution)
    print('base columns = ', self.base_columns)


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
            self.vero[i,:] /= aux
        for j in range(self.dimension[0]):                           # For each line
            if (i != j):                                             # It's not the basic variable line
                aux = copy.deepcopy(self.A[j][self.base_columns[i]]) # Value that should be null
                self.A[j,:] -= aux * self.A[i,:]                     # Subtract all the line
                self.b[j] -= aux * self.b[i]                         # Vector b is also subtracted
                self.vero[j,:] -= aux * self.vero[i, :]
        aux = self.c[self.base_columns[i]]                           # c input must also be null
        self.c -= aux * self.A[i,:]                                  # Substract all the vector c
        self.optimal_solution -= aux * self.b[i]                     # Substract the optimal value with respect to vector b
        self.certificate -= aux * self.vero[i,:]
    vfunc = np.vectorize(rounding_to_zero)                           # Applies the function in parameter in all the vector's input
    self.A = vfunc(self.A)                                           # (set very low values to zero)
    self.b = vfunc(self.b)
    self.c = vfunc(self.c)
    self.optimal_solution = vfunc(self.optimal_solution)
    self.certificate = vfunc(self.certificate)
    self.vero = vfunc(self.vero)


# Following Bland's rule, find the pivot element in the correct column and line and check if it's an unbounded LP
def find_pivot(self):
    for i in range(self.dimension[1]):                              # For each column
        is_unbounded = False
        pivot_column = i                                            # Pivot column index
        pivot_row = 0                                               # Pivot row index
        if(self.c[i] < 0):                                          # Negative input in c found
            c_aux = copy.deepcopy(self.c)
            c_aux = np.delete(c_aux, [i])
            # Checking unbounded PL
            if(np.all(self.A[:, i] <= 0) and (np.all(c_aux >= 0) or i < self.dimension[1] - self.dimension[0])):
                is_unbounded = True
                break                                               # Computing optimal value is impossible
            if(self.c[i] < 0):
                min_value = 100                                     # Maximum value for all the constraint variables
                for j in range(self.dimension[0]):                  # Find the minimum value for all the lines in this column
                    if(self.A[j][i] != 0):
                        candidate_value = self.b[j] / self.A[j][i]  # The minimum value is the new pivot
                        if(candidate_value < min_value and candidate_value >= 0 and self.A[j][i] > 0):
                            min_value = candidate_value             # The current minimum value
                            pivot_row = j                           # The current pivot row index
                break                                               # New pivot is found
    return pivot_column, pivot_row, is_unbounded


# Find the solution for the basic variables
def find_solution(self):
    solution = np.zeros(self.dimension[1] - self.dimension[0])      # The solution size is the original number of variables
    for i in range(len(self.b)):
        if(self.base_columns[i] < self.dimension[1] - self.dimension[0]):
            solution[self.base_columns[i]] = self.b[i]
    return solution                                                 # Vector with the optimal values for the basic variables


# Simplex algorithm
def simplex(constraints, result_constraints, objective_function, base_indexes, vero):
    tableau = Tableau()                                             # Create a tableau with the received data
    tableau.A = copy.deepcopy(constraints)
    tableau.b = copy.deepcopy(result_constraints)
    tableau.c = objective_function * (-1)
    tableau.base_columns = copy.deepcopy(base_indexes)
    tableau.dimension = (constraints.shape[0], constraints.shape[1])
    tableau.certificate = np.zeros(tableau.dimension[0])
    tableau.vero = vero.copy()
    canonical_form(tableau)
    while(np.any(tableau.c < 0)):                                   # Vector c has negative values
        pivot_column, pivot_row, is_unbounded = find_pivot(tableau) # Find the element to be the new pivot
        if(is_unbounded):                                           # The LP is unbounded
            tableau.identification = 'ilimitada'
            solution = find_solution(tableau)                       # Find a not optimal solution (does not exist)
            return tableau.certificate, tableau.optimal_solution, solution, tableau.identification, tableau.base_columns
        tableau.base_columns[pivot_row] = pivot_column              # Update the base columns
        canonical_form(tableau)                                     # Update the tableau for canonical form again
    solution = find_solution(tableau)                               # Find the optimal solution
    if(tableau.optimal_solution < 0):                               # When optimal solution is negative, the LP is inviable
        tableau.identification = 'inviavel'
    else:                                                           # This LP has an optimal solution
        tableau.identification = 'otima'
    return tableau.certificate, tableau.optimal_solution, solution, tableau.identification, tableau.base_columns


# When there is no base in original pl, find them using an auxiliar pl
def auxiliar_pl(inicial_A, inicial_b):
    aux_A = copy.deepcopy(inicial_A)
    aux_b = copy.deepcopy(inicial_b)
    # Concatenate an identity matrix to the original one
    aux_A = np.concatenate((aux_A, np.eye(inicial_A.shape[0], dtype = float)), axis = 1)
    # The auxiliar c vector has 0 in original inputs and -1 in new inputs
    aux_c = np.concatenate((np.zeros(inicial_A.shape[1]), np.full(inicial_A.shape[0], -1)))
    # The base indexes for auxiliar pl
    aux_base_indexes = list(range(inicial_A.shape[1], inicial_A.shape[0] + inicial_A.shape[1]))
    return aux_A, aux_b, aux_c, aux_base_indexes


# For printing the array solution
def print_array(a):
    for i in range(len(a)):
        print('{:.7f}'.format(a[i]), end=' ')
    print()


#----------------------------------------------------- Execution ------------------------------------------------------------
# Receiving data
N, M = input().split()                                               # The input format is specified in READ_ME
N = int(N)                                                           # Constraints number
M = int(M)                                                           # Variables number

input_c = input().split()                                            # Objective function input
c_optimal_input = np.array(input_c, dtype = float)

constraints_input = []
for i in range(N):                                                   # Constraints input
    constraints_input.append(input().split())
constraints_input = np.array(constraints_input, dtype = float)

fpi_variables = np.eye(N, dtype = float)                             # An identity matrix of size N (a new variable for each inequal constraint)

vero_matrix = np.eye(N, dtype = float)

b_input = np.array(constraints_input[:,-1])                          # Constraints results input

if(np.array_equal(constraints_input[:, (N - 1):-1], fpi_variables)): # The LP already has a base
    base_input = list(range(M - N, M))                               # The basic variables are the fpi ones
else:                                                                # No base was formed with the fpi format
    base_input = list(range(M, M + N))                               # The bases are the compensating variables

# Add the fpi variables for making LP fpi form
constraints_input = np.concatenate((np.array(constraints_input[:,:-1]), fpi_variables), axis = 1)
c_optimal_input = np.concatenate((np.array(input_c, dtype = float), np.zeros(N)))

# Check on negative values in b vector
negative_b = False
if(np.any(b_input < 0)):
    negative_b = True
    for i in range(N):
        if(b_input[i] < 0):
            b_input[i] *= (-1)                                       # Multiply the b negative row by (-1)
            constraints_input[i][:] *= (-1)
            vero_matrix[i][:] *= -1

# Create an solve auxiliar pl for the original problem
aux_A, aux_b, aux_c, aux_base_indexes = auxiliar_pl(constraints_input, b_input)
aux_certificate, aux_optimal_value, aux_solution, aux_identification, aux_base_indexes = simplex(aux_A, aux_b, aux_c, aux_base_indexes, vero_matrix.copy()) 

if(aux_optimal_value < 0):                                           # When auxiliar PL has a negative optimal value, the original problem is impossible
    print(aux_identification)
    print(aux_certificate)
else:
    if(negative_b):                                                  # When the original problem has negative b values, there is no original base
        aux_base_indexes.sort()                                      # because the row is multiplied by (-1), so use the auxiliar pl to find them
        aux_base_indexes = aux_base_indexes[:N + M]
        for i in range(len(aux_base_indexes)):
            if(aux_base_indexes[i] > M + N):                         # If the basic variable is an auxiliar variable in auxiliar pl
                aux_base_indexes[i] = aux_base_indexes[i] - (M + N)
        base_input = aux_base_indexes
    last_certificate, last_optimal_value, last_solution, last_identification, last_base_columns = simplex(constraints_input, b_input, c_optimal_input, base_input, vero_matrix)
    v_func = np.vectorize(rounding_to_zero)
    solution = v_func(last_solution)
    optimal_value = v_func(last_optimal_value)
    print(last_identification)
    if(last_identification == 'ilimitada'):
        print_array(last_solution)
    if(last_identification == 'otima'):
        print('{:.7f}'.format(last_optimal_value))
        print_array(last_solution)
        print_array(last_certificate)