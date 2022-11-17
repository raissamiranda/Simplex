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

n m

c_{1} c_{2} ... c_{m} 

a_{1,1} a_{1,2} ... a_{1,m} b_{1}

a_{2,1} a_{2,2} ... a_{2,m} b_{2}

...     ...     ...     ...     ...

a_{n,1} a_{n,2} ... a_{n,m} b_{n}

with:

$1 \le n \le 100
1 \le m \le 100
\forall i; 1 \le i \le n; \forall j; 1 \le j \le m; |a_{i,j}| j \le 100
\forall i; 1 \le i \le m; |b_{i}| \le 100
\forall i; 1 \le i \le m; |c_{i}| \le 100$



