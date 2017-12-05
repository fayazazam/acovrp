import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pandas.tools.plotting import parallel_coordinates

file = 'benchmark.csv'
cols =	['alpha','beta','q0','m','best']
data = pd.read_csv(file, names=cols)

y = data['m']
X = data.ix[:]

z = np.polyfit(X[y==5]['alpha'], X[y==5]['best'], 2)
f = np.poly1d(z)

# calculate new x's and y's
x_new = np.linspace(X[y==5]['alpha'].min(), X[y==5]['alpha'].max(), 50)
y_new = f(x_new)

plt.plot(x_new,y_new,c='red')

plt.scatter(X[y==5]['alpha'], X[y==5]['best'], label='M = 5', c='red')
plt.scatter(X[y==15]['alpha'], X[y==15]['best'], label='M = 15', c='blue', alpha=0.1)
plt.scatter(X[y==25]['alpha'], X[y==25]['best'], label='M = 25', c='green', alpha=0.1)

plt.legend()
plt.xlabel('alpha')
plt.ylabel('best')

plt.show()