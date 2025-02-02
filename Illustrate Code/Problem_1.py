import gurobipy
import numpy as np
from numpy import random

#Create matrix A 8x5
n=8
m=5
A = np.array([
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
    np.random.randint(low=1,high=10,size=m),
])

#Create matrix B 5x1
b = np.array([np.random.randint(50,150),
             np.random.randint(50,150),
             np.random.randint(50,150),
             np.random.randint(50,150),
             np.random.randint(50,150)])

#Create array l with size 8
l = np.array([np.random.randint(low=100,high=200,size=n)])

#Calculate the selling cost
q = np.matmul(A,b)+l + np.array([np.random.randint(low=200,high=400,size=n)])

#create array S of size 5 with random 5 integer values.
s = np.array([np.random.randint(1,10),
             np.random.randint(1,10),
             np.random.randint(1,10),
             np.random.randint(1,10),
             np.random.randint(1,10)])

#create array D of size 8 representing the results of a binomial random variable based on binomimal distribution.
D = np.array([np.random.binomial(10,0.5,8),np.random.binomial(10,0.5,8)])

#Print the input solution for the model
print("The matrix A size 8x5 with 8 is products and j is suppliers:  ")
print(A)
print("The random demand D for the product:")
print(D)
print("The selling price of the product:")
print(q)
print("The preorder cost b:")
print(b)
print("The salvage value s:")
print(s)
print("The addition cost l:")
print(l)

#Setting up an optimization model in Gurobipy
firststage=gurobipy.Model("S2P")
firststage.ModelSense=gurobipy.GRB.MINIMIZE
firststage.setParam('OutputFlag',0)

#Adding new variables x, y1 and z1
x = firststage.addMVar((m,1), vtype = gurobipy.GRB.INTEGER, name = "x")
y1 = firststage.addMVar((m,2), vtype = gurobipy.GRB.INTEGER, name = "y1")
z1 = firststage.addMVar((n,2), vtype = gurobipy.GRB.INTEGER, name = "z1")

#Add necessary constraints for the model
firststage.addConstr(x>=0)
firststage.addConstr(y1>=0)
firststage.addConstr(z1>=0)
firststage.addConstr(z1<=D.T)
firststage.addConstr(y1 == x - A.T @ z1)

#Minimize the equation calculated based on the variables x,y1, z1 and the data vectors b, l, q, s
firststage.setObjective(b.T @ x + gurobipy.quicksum(((l-q) @ z1[:,k] - s @ y1[:,k])*0.5 for k in range(2)))
firststage.optimize()

#Storing output results in x_value, y1_value and z1_value
x_value = x.x
y1_value = y1.x
z1_value = z1.x

#Print the optimized resutls after minimize the model
print("Optimal Solution:")
print('Obj: %g' % firststage.objVal)
print(f"x = {x_value}")
print(f"y1 = {y1_value}")
print(f"z1 = {z1_value}")