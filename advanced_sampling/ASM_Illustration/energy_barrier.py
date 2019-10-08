import numpy as np
import os
import imageio
import natsort
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import rc


def FES(x):
    """
    This function calculates the value(s) of free energy given the value(s) of CV.

    Parameters
    ----------

    x : float or np.array
        value of CV

    Returns
    -------

    y : float or np.array
        value of free energy

    Examples
    --------

    >>> FES(1.822)
    2.390088592634875

    >>> FES(np.arange(0,10,1))
    array([6.84595   , 2.55345581, 2.63137371, 4.87913363, 7.07697797,
           7.7159    , 6.38054805, 3.78509539, 1.46207595, 1.10418573])
    """

    coef = [-0.000481992, 0.0133127, -0.102597, -
            0.0406179, 2.84049, -7.0026, 6.84595]
    y = 0
    for i in range(len(coef)):
        y += coef[i] * x ** (6 - i)
    return y


def circle_on_FES(a, b, r):
    """
    This output the coordinates of a circle on the surface given the coordinates of the center.

    Parameters
    ----------

    a : float
        x coordinate of the center of the circle
    b : float
        y coordinate of the center of the circle
    r : float
        The radius of the circle

    Returns
    -------

    rx : np.array
        x coordaintes of the circle
    ry : np.array
        y coordinates of the circle

    Examples
    --------

    >>> circle_on_FES(1,2,3)
    (array([ 4.        ,  3.99396003,  3.97586444,  3.94578609,  3.9038461 ,
        3.85021335,  3.7851038 ,  3.70877961,  3.62154813,  3.5237606 ,
        3.41581077,  3.29813333,  3.17120211,  3.03552823,  2.891658  ,
        2.74017073,  2.5816764 ,  2.41681322,  2.24624504,  2.07065866,
        1.89076113,  1.70727681,  1.52094453,  1.3325146 ,  1.14274575,
        0.95240211,  0.76225013,  0.57305549,  0.38558   ,  0.20057856,
        0.01879611, -0.15903538, -0.33219984, -0.5       , -0.66176019,
       -0.81682906, -0.9645822 , -1.10442466, -1.23579335, -1.35815928,
       -1.47102974, -1.57395024, -1.66650635, -1.74832537, -1.81907786,
       -1.87847892, -1.92628936, -1.96231667, -1.98641577, -1.99848963,
       -1.99848963, -1.98641577, -1.96231667, -1.92628936, -1.87847892,
       -1.81907786, -1.74832537, -1.66650635, -1.57395024, -1.47102974,
       -1.35815928, -1.23579335, -1.10442466, -0.9645822 , -0.81682906,
       -0.66176019, -0.5       , -0.33219984, -0.15903538,  0.01879611,
        0.20057856,  0.38558   ,  0.57305549,  0.76225013,  0.95240211,
        1.14274575,  1.3325146 ,  1.52094453,  1.70727681,  1.89076113,
        2.07065866,  2.24624504,  2.41681322,  2.5816764 ,  2.74017073,
        2.891658  ,  3.03552823,  3.17120211,  3.29813333,  3.41581077,
        3.5237606 ,  3.62154813,  3.70877961,  3.7851038 ,  3.85021335,
        3.9038461 ,  3.94578609,  3.97586444,  3.99396003,  4.        ]), array([5.        , 5.19027176, 5.37977736, 5.56775373, 5.75344396,
       5.93610034, 6.11498737, 6.28938474, 6.45859021, 6.62192245,
       6.77872379, 6.92836283, 7.07023703, 7.20377513, 7.32843939,
       7.44372786, 7.54917629, 7.64436009, 7.72889599, 7.80244358,
       7.86470672, 7.9154347 , 7.95442326, 7.98151539, 7.99660202,
       7.99962238, 7.99056433, 7.96946433, 7.93640734, 7.89152648,
       7.83500246, 7.76706288, 7.68798132, 7.59807621, 7.49770956,
       7.38728552, 7.26724872, 7.13808251, 7.000307  , 6.85447696,
       6.70117959, 6.54103217, 6.37467957, 6.20279161, 6.02606043,
       5.84519767, 5.6609316 , 5.47400419, 5.28516813, 5.0951838 ,
       4.9048162 , 4.71483187, 4.52599581, 4.3390684 , 4.15480233,
       3.97393957, 3.79720839, 3.62532043, 3.45896783, 3.29882041,
       3.14552304, 2.999693  , 2.86191749, 2.73275128, 2.61271448,
       2.50229044, 2.40192379, 2.31201868, 2.23293712, 2.16499754,
       2.10847352, 2.06359266, 2.03053567, 2.00943567, 2.00037762,
       2.00339798, 2.01848461, 2.04557674, 2.0845653 , 2.13529328,
       2.19755642, 2.27110401, 2.35563991, 2.45082371, 2.55627214,
       2.67156061, 2.79622487, 2.92976297, 3.07163717, 3.22127621,
       3.37807755, 3.54140979, 3.71061526, 3.88501263, 4.06389966,
       4.24655604, 4.43224627, 4.62022264, 4.80972824, 5.        ]))
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    rx = r * np.cos(theta) + a
    # the circle should always be on the surface
    ry = r * np.sin(theta) + b + r

    return rx, ry


if __name__ == '__main__':

    os.mkdir('images_barrier')

    # Data for plotting free energy surface
    CV = np.arange(0, 12.1, 0.1)
    fes = FES(CV)

    # Metropolis-Hasting algorithm
    x = 1.44908    # initial value of x (y = 1.827) at minmium of FES
    y = FES(x)
    n_trial = 200
    max_d = 0.8   # max displacement
    for i in range(n_trial):
        delta_x = (2 * np.random.rand(1) - 1) * \
            max_d  # -1 <= delta_x/max_d <= 1
        x_proposed = x + delta_x
        y_proposed = FES(x_proposed)
        delta_y = y_proposed - y
        p_acc = np.exp(-delta_y)  # beta = 1
        r = np.random.rand(1)
        # print('delta_x:', delta_x)

        if r < p_acc:   # move accepted
            x += delta_x   # update x
            y = FES(x)     # update y
        # print(x)

        # Data for plotting circles
        rx, ry = circle_on_FES(x, y, 0.2)  # initial position: minimum of FES
        # print([rx,ry])

        rc('font', **{
            'family': 'sans-serif',
            'sans-serif': ['DejaVu Sans'],
            'size': 10,
            'weight': 'bold'
        })
        # Set the font used for MathJax - more on thiprint(images)
        rc('mathtext', **{'default': 'regular'})
        plt.rc('font', family='serif')

        plt.figure()
        ax = plt.axes(xlim=(0, 12), ylim=(0, 9))
        plt.plot(CV, fes, zorder=5, linewidth=2)
        plt.plot(rx, ry, color='black', zorder=10)
        plt.fill(rx, ry, color='yellow', zorder=10)
        plt.fill_between(CV, 0, fes, color='steelblue')
        plt.xlabel('Centers of mass separation distance (nm)',
                   fontsize='12', fontweight='bold')
        plt.ylabel('Free energy ($k_{B} T$)', fontsize='12', fontweight='bold')
        plt.title('Normal MD simulations', fontsize='14', fontweight='bold')
        plt.minorticks_on()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.05)
        plt.savefig('./images_barrier/energy_barrier_%s.png' % (i))
        # to prevent the warning of opening plots over 20 times
        plt.close('all')

    images = []
    filenames = natsort.natsorted(os.listdir('./images_barrier'), reverse=False)
    # get the filenames and order them in the ascending order

    for filename in filenames:
        if filename.endswith('.png'):
            file_path = os.path.join('./images_barrier', filename)
            images.append(imageio.imread(file_path))
    imageio.mimsave('./energy_barrier_redo.gif', images, duration=0.05)

    os.system('rm -r images_barrier')
