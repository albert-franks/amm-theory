'''
Import libraries
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
'''
User defined inputs
'''
N_x = 100
N_y = 400000
plot_trade_size = '0.01'
normalize_price_impact = False
'''
Methods
'''
def get_L2(N_x, N_y): return N_x*N_y
def get_dy(N_x, N_y, dx): return (N_y*dx)/(N_x - dx)
def calculate_price_impact(N_x, N_y, dx, dy): return dy - (N_y/N_x)*dx
'''
State-space construction
'''
def analyse_price_impact(min_N_x, max_N_x, step_N_x, L2, plot_trade_size, normalize_price_impact):
    '''
    Build the constant product curve
    '''
    N_x_range = np.arange(min_N_x, max_N_x + step_N_x, step_N_x)
    N_y_range = L2/N_x_range
    fraction_of_X_reserves_taken = np.arange(-0.5, 0.5 + 0.01, 0.01)
    data = np.zeros((len(N_x_range), 3 + len(fraction_of_X_reserves_taken)))
    for ix in range(len(N_x_range)):
        p = N_y_range[ix]/N_x_range[ix]
        data[ix,0:3] = [N_x_range[ix], N_y_range[ix], p]
        for ij in range(len(fraction_of_X_reserves_taken)):
            dx = fraction_of_X_reserves_taken[ij]*N_x
            dy = get_dy(N_x, N_y, dx)
            I = calculate_price_impact(N_x, N_y, dx, dy)
            if normalize_price_impact:
                I /= p
            data[ix,3+ij] = I
    columns_names = list(map('{:.2f}'.format, fraction_of_X_reserves_taken))
    dataframe = pd.DataFrame(data=data,columns = ['N_x','N_y','p'] + columns_names)
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(dataframe['N_x'], dataframe['N_y'], dataframe[plot_trade_size], c = dataframe['0.01'],cmap='viridis')
    '''
    Set labels and titles
    '''
    ax.set_xlabel(r'$X$ (units)')
    ax.set_ylabel(r'$Y$ (units)')
    ax.zaxis.set_rotate_label(False) 
    if normalize_price_impact:
        ax.set_zlabel(r'$\mathcal{I} / p$', rotation = 90)
        ax.set_title(r'Uniswap v2 price impact (as a fraction of the spot price $p$) of a trade taking {:.0f}% of token $X$ reserves'.format(100*float(plot_trade_size)))    
    else:
        ax.set_zlabel(r'$\mathcal{I}$', rotation = 90)
        ax.set_title(r'Uniswap v2 price impact (in units of $Y$) of a trade taking {:.0f}% of token $X$ reserves'.format(100*float(plot_trade_size)))
    plt.show()
analyse_price_impact(50, 200, 0.5, get_L2(N_x,N_y),plot_trade_size,normalize_price_impact)
