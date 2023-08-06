'''
Import libraries
'''
import numpy as np
import matplotlib.pyplot as plt
'''
User defined inputs
'''
N_x = 100
N_y = 400000
L2 = N_x*N_y
'''
State-space construction
'''
def plot_statespace(min_N_x, max_N_x, step_N_x, L2):
    N_x_range = np.arange(min_N_x, max_N_x + step_N_x, step_N_x)
    N_y_range = L2/N_x_range
    fig, ax = plt.subplots()
    ax.plot(N_x_range, N_y_range, color = 'black')
    ax.set_xlabel(r'$X$ (units)')
    ax.set_ylabel(r'$Y$ (units)')
    ax.set_title(r'Uniswap v2 state-space. $L^2$ = {0}'.format(L2))
    plt.show()

plot_statespace(0, 1000, 10, L2)
