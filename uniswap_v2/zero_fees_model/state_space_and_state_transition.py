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
dx =  20
'''
Retrieve relevant quantities from canonical formulae of the uniswap v2 framework
'''
dy = (N_y*dx)/(N_x - dx)
L2 = N_x*N_y
'''
State-space construction
'''
def plot_statespace(min_N_x, max_N_x, step_N_x, L2, ex_ante_state, variations):
    '''
    Build the constant product curve
    '''
    N_x_range = np.arange(min_N_x, max_N_x + step_N_x, step_N_x)
    N_y_range = L2/N_x_range
    fig, ax = plt.subplots()
    ax.plot(N_x_range, N_y_range, color = 'red',label = r'$XY = L^2$',linewidth=2,zorder=6)
    ex_post_state = [ex_ante_state[0] - variations[0], ex_ante_state[1] + variations[1]]
    '''
    Plot the spot price, i.e., the line connecting the origin and the ex-ante state-space
    '''
    spot_price = ex_ante_state[1]/ex_ante_state[0]
    ax.plot(N_x_range[N_x_range <= ex_ante_state[0]], 
            N_x_range[N_x_range <= ex_ante_state[0]]*(spot_price),
            linewidth = 2, label =r'$p$',zorder=5)
    '''
    Plot the tangent line at the ex-ante state space
    '''
    tangent_line_slope = -L2/(ex_ante_state[0]**2)
    ax.plot(N_x_range, ex_ante_state[1] + (N_x_range - ex_ante_state[0])*tangent_line_slope,
            linewidth = 2, label='tangent', zorder = 4)
    '''
    Plot changes in pool reserves
    '''
    ax.plot([ex_ante_state[0], ex_post_state[0]], 
            [ex_ante_state[1], ex_ante_state[1]], 
            linewidth = 2, label = r'$\Delta X$',
            color = 'black', zorder=3,
            marker = '<' if variations[0] > 0 else '>')
    ax.plot([ex_ante_state[0], ex_ante_state[0]],
            [ex_ante_state[1], ex_post_state[1]],
            linewidth = 2, label = r'$\Delta Y$',
            color = 'black', zorder=3,
            marker = '^' if variations[0] > 0 else 'v')
    '''
    Plot projections of the lines created above
    '''
    ax.plot([ex_ante_state[0], ex_post_state[0]], 
            [ex_post_state[1], ex_post_state[1]],    
            linewidth = 1, color = 'gray', linestyle = 'dashed',zorder=1)
    ax.plot([ex_post_state[0], ex_post_state[0]], 
            [ex_ante_state[1], ex_post_state[1]],    
            linewidth = 1, color = 'gray', linestyle = 'dashed',zorder=1)
    '''
    Plot the impact of the trade and the hypothetical change in Y in an impact-free system
    '''
    ax.plot([ex_post_state[0],ex_post_state[0]],
            [ex_ante_state[1],ex_ante_state[1] + (ex_post_state[0] - ex_ante_state[0])*tangent_line_slope],
             linewidth = 2, color = 'violet',label=r'$\Delta Y^{\mathcal{I} = 0}$',zorder=2)
    ax.plot([ex_post_state[0],ex_post_state[0]],
            [ex_ante_state[1] + (ex_post_state[0] - ex_ante_state[0])*tangent_line_slope, ex_post_state[1]],
             linewidth = 2, color = 'green',label=r'$\mathcal{I}$',zorder=2)
    '''
    Plot the ex-ante state
    '''
    ax.plot(ex_ante_state[0], ex_ante_state[1], color = 'black',marker='o',markersize = 7.5, zorder = 7)
    ax.annotate(r'$\mathcal{P}$', (ex_ante_state[0]*1.005, ex_ante_state[1]*1.005), fontsize = 16) 
    '''
    Plot the ex-post state
    '''
    ax.plot(ex_post_state[0], ex_post_state[1], color = 'black',marker='o',markersize = 7.5, zorder = 7)
    ax.annotate(r'$\mathcal{P}^{\,\prime}$', (ex_post_state[0]*1.005, ex_post_state[1]*1.005), fontsize = 16)
    '''
    Set axis limits
    '''
    ax.set_xlim([0.99*np.minimum(ex_ante_state[0],ex_post_state[0]) - abs(variations[0]), 1.01*np.maximum(ex_ante_state[0],ex_post_state[0]) + abs(variations[0])])
    ax.set_ylim([0.99*np.minimum(ex_ante_state[1],ex_post_state[1]) - abs(variations[1]), 1.01*np.maximum(ex_ante_state[1],ex_post_state[1]) + abs(variations[1])])
    '''
    Set labels and titles
    '''
    ax.set_xlabel(r'$X$ (units)')
    ax.set_ylabel(r'$Y$ (units)')
    ax.set_title(r'Uniswap v2 state-space. $L^2$ = {0}'.format(L2))
    '''
    Add a legend
    '''
    ax.legend()
    plt.show()

plot_statespace(0, 1000, 1, L2, [N_x,N_y], [dx,dy])
