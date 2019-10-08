#!/usr/bin/env python
"""
This is a python code to check the convergence of 1D PMF curve by plotting RMSD compared with the
curve at the previous time frame as a function of time.
"""

import argparse
import os
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np



def initialize():
    parser = argparse.ArgumentParser(
        description='Outplot a plot of RMSD vs time')
    parser.add_argument('-f',
                        '--hills',
                        help='File name of the HILLS file.')
    parser.add_argument('-s',
                        '--stride',
                        help='Stride (number of Gaussians) for the PLUMED function sum_hills')
    parser.add_argument('-ng',
                        '--gaussian',
                        help='Number of Gaussians deposited every ns')
    parser.add_argument('-n',
                        '--pngname',
                        type=str,
                        help='The filename of the image without an extension (format: RMSD_fes' /
                        'user-defined.png)')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = initialize()

    # Generate multiple fes.dat files
    os.system("plumed sum_hills --hills %s --stride %s --mintozero" %
              (args.hills, args.stride))
    n = 0     # number of the output files (fes_*.dat)
    while os.path.isfile('fes_%s.dat' % n):
        n += 1

    # Read in the data of all files and preprocess them
    for i in range(n):
        fes = []
        infile = open('fes_%s.dat' % i, 'r')
        lines = infile.readlines()
        infile.close
        # Parse data
        m = 0
        for line in lines:
            if line[0] == '#' or line[0] == '@':
                m += 1  # number of parameter lines
        # read in data starting from (m+1)-th line to the end
        for line in lines[m:]:
            if line[0] != '#' and line[0] != '@':
                tokens = line.split()
                fes.append(float(tokens[1]))
        if i == 0:
            fes_data = np.zeros([n, len(fes)])
        fes_data[i] = fes   # units: kcal/mol

    T = 298.15
    conversion = 1.38064852 * 6.02 * T / 1000  # from kcal/mol to kT
    fes_data = fes_data / conversion

    # Now start to calculate RMSD
    d_squared = 0
    RMSD, t = np.zeros(n), np.zeros(n)
    ref = fes_data[-1]    # Use the last time frame as the reference
    # delta t between fes_*.dat files
    delta_t = float(args.stride)/float(args.gaussian)
    for i in range(n):
        d_squared = 0
        for j in range(len(fes)):
            d_squared += (fes_data[i][j]-ref[j])**2
        RMSD[i] = np.sqrt(d_squared/len(fes))
        # It's fine that last time frame (ref) is not delta_t*n. We're not plotting it.
        t[i] = delta_t*(i+1)
    t = t[:-1]
    RMSD = RMSD[:-1]

    # Ready to plot!
    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
    })

    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    fig, ax = plt.subplots()
    #fig, ax = plt.subplots(figsize=(9,6))
    plt.plot(t, RMSD)    # The last point is zero and we don't plot it
    plt.scatter(t, RMSD, marker='o', c='r')
    plt.gca().set_xlim(right=max(t) + 0.1 * (max(t) - min(t)))
    plt.xlabel("Simulation time (ns)")
    plt.ylabel("RMSD of free energy ($ k_{B} T$)")
    plt.title("RMSD of free energy as a function of time")
    plt.text(0.53, 0.94, "(Reference: the last time frame)",
             transform=ax.transAxes)
    for i, j in enumerate(RMSD):  # label the values (check the enumerate function!)
        ax.text(t[i] + 0.01 * (max(t) - min(t)), j + 0.01 *
                (max(RMSD) - min(RMSD)), "{0:.2f}".format(j), size='8')
    plt.minorticks_on()
    plt.grid()

    plt.savefig('RMSD_fes_%s.png' % args.pngname)
    plt.show()

    os.system("rm fes_*.dat")
