#!/usr/bin/env python
"""
This is a Python code specific to plot 2D PMF based on data from metadynamics with units of energy as kT.
"""

import argparse 
import matplotlib.pyplot as plt
import numpy as np
import os.path
from matplotlib import rc

def initialize():
    parser = argparse.ArgumentParser(
            description='This code saves a contour plot of FES based on data from metadynamics.')
    parser.add_argument('-f',
                        '--dat',
                        help='Name of the input .dat file')
    parser.add_argument('-nx',
                        '--xbins',
                        help='Number of bins of x')
    parser.add_argument('-ny',
                        '--ybins',
                        help='Number of bins of y')
    parser.add_argument('-nl',
                        '--nlines',
                        help='Number of contour lines')
    parser.add_argument('-x',
                        '--xlabel',
                        type=str,
                        help='The name and units of x-axis')
    parser.add_argument('-y',
                        '--ylabel',
                        type=str,
                        help='The name and units of y-axis')
    parser.add_argument('-t', '--title', type=str, help='Title of the plot')
    parser.add_argument('-n',
                        '--pngname',
                        type=str,                                                   
                        help='The filename of the image without an extension')

    args_parse = parser.parse_args()

    return args_parse

if __name__=='__main__':

    args = initialize()

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    x, y, f = [], [], [] # f=f(x,y). Namely, FES=FES(CV1, CV2)
    infile = open('%s' % args.dat, 'r')
    lines = infile.readlines()
    infile.close

    #Parse data
    
    n = 0
    m = 0
    for line in lines[m:]:
        if line[0] != '#' and line[0] != '@':
            tokens = line.split()
            if tokens != []:
                x.append(float(tokens[0]))
                y.append(float(tokens[1]))
                f.append(float(tokens[2]))
    

    x = np.array(x).reshape(int(args.xbins), int(args.ybins))  # projetion
    y = np.array(y).reshape(int(args.xbins), int(args.ybins))  # angle
    f = np.array(f).reshape(int(args.xbins), int(args.ybins))  # FES
    cos_y = np.cos(y)  # cosine of the angle
    
    T = 298.15
    conversion_y = np.pi/180  # from radian to degree
    conversion_f = 1.38064852 * 6.02 * T / 1000 # from kcal/mol to kT

    y = y / conversion_y
    f = f / conversion_f

    max_f = int(np.floor(f.max()))      
    fig, ax = plt.subplots(figsize=(9,6))
    CS = ax.contourf(x, y, f, int(args.nlines))
    CS1 = ax.contour(CS, levels=CS.levels)
    plt.title('%s' % args.title)
    plt.xlabel('%s' % args.xlabel)
    plt.ylabel('%s' % args.ylabel)
    plt.grid(True)
    plt.colorbar(CS)

    plt.savefig('%s.png' % args.pngname)

    # Save the image, but not overwrite the file with the same file name.
    # The name of the file should be 'pic.png', 'pic_1.png', ...
    """
    n = 0   # number of the figures that have been produce in the same dir.
    while os.path.isfile('%s_%s.png' % (args.pngname, n)):
        n += 1
    plt.savefig('%s_%s.png' % (args.pngname, n))
    """

    plt.show()
