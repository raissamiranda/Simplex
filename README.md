# Simplex

Simplex algorithm is used to solve the Linear Programming (LP) optimization problems. 

## Description

This project solves linear problems in canonical form:
> max $c^Tx$
> 
> subject to $Ax \le b$

with $c$ the coefficients of the objective function, $A$ and $b$ represents the constraints with a $m x n$ matrix and an array.

$$
A = \left[
\begin{array}{cccc}
a_{1,1} & a_{1,2} & ... & a_{1,m} \\
a_{2,1} & a_{2,2} & ... & a_{2,m} \\
... & ... & ... & ... \\
a_{n,1} & a_{n,2} & ... & a_{n,m} \\
\end{array}
\right]
$$

$$
b = \left[
\begin{array}{c}
b_{1} \\
b_{2} \\
... \\
b_{n} \\
\end{array}
\right]
$$

$$
c = \left[
\begin{array}{c}
c_{1} \\
c_{2} \\
... \\
c_{m} \\
\end{array}
\right]
$$

## Input
The first line of the input contains two integers n and m, respectively the number of constraints and variables.

The second line contains m integers, that represents vector $c$.

Each of the next n lines contains m + 1 integers that represents the constraints. The first m lines are the A matrix and the last column in b vector.

The values, including, b can be negative.

There is an example for a generic input below:

$n$  $m$

$c_{1} c_{2} ... c_{m} $

$a_{1,1} a_{1,2} ... a_{1,m} b_{1}$

$a_{2,1} a_{2,2} ... a_{2,m} b_{2}$

$...     ...     ...     ...     ...$

$a_{n,1} a_{n,2} ... a_{n,m} b_{n}$


with:

$1 \le n \le 100$

$1 \le m \le 100$

$\forall i; 1 \le i \le n; \forall j; 1 \le j \le m; |a_{i,j}| j \le 100$

$\forall i; 1 \le i \le m; |b_{i}| \le 100$

$\forall i; 1 \le i \le m; |c_{i}| \le 100$


## Output

* If there is an optimal value, the first line contains "otima", the second the optimal value and the third a solution that reaches the maximum value.

* If it's an infeasible LP, the first line contains "inviavel".

* If it's an unlimited LP, the first line contains "ilimitada" and the second a viable solution.


## Examples

### Input 1:
```
3 3
2 4 8
1 0 0 1
0 1 0 1
0 0 1 1
```

### Output 1:
```
otima
14
2 4 8
```

### Input 2:
```
4 3
1 1 1
1 0 0 -1
0 1 0 -1
0 0 1 -1
1 1 1 -1
```

### Output 2:
```
inviavel
```

### Input 3:
```
2 3
1 0 0
-1 1 0 5
-1 0 1 7
```

### Output 3:
```
ilimitada
0 5 7
```

### Input 4:
```
4 4
-3 -4 5 -5
1 1 0 0 5
-1 0 -5 5 -10
2 1 1 -1 10
-2 -1 -1 1 -10
```

### Output 4:
```
otima
50
0 0 5 0
```



