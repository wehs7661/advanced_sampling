#!/usr/bin/env python
"""
This Python code can be used to extract one or more structure files (like .pdb or .gro file) from
trajectory file (like a .trr or .xtc file). This code is useful when the trajectory file is from
a metadynamics simulation. Given the COLVAR file, the user can specify the threshold value of the
CV (using -c flag) and output the structure file at time frames with CV larger than the threshold.
"""

import argparse
import os
import numpy as np


def initialize():
    parser = argparse.ArgumentParser(
        description='Extract pdb files at certain time frames from one trajectory')
    parser.add_argument('-f',
                        '--trj',
                        help='The file name of any types of trajectory file')
    parser.add_argument('-s',
                        '--tpr',
                        help='The file name of the structure file (like .gro or .tpr)')
    parser.add_argument('-t',
                        '--time',
                        nargs='+',
                        help='The time frame [ps] to output')
    parser.add_argument('-p',
                        '--prefix',
                        nargs='?',
                        help='The prefix of the output file (default: prefix of the input')
    # the default of prefix is set in the if statement below
    parser.add_argument('-c',
                        '--CV',
                        nargs='?',
                        help='The threshold value of CV. A COLVAR file is required.')
    parser.add_argument('-cf',
                        '--CVfile',
                        nargs='?',
                        help='The file name of the COLVAR file.')
    parser.add_argument('-m',
                        '--mpi',
                        default=False,
                        action='store_true',  # store boolean True instead of 'False'
                        help='Whether the MPI-version of GROMACS is used.')

    args_parse = parser.parse_args()

    # Below we set the default to some optional arugments (nargs='?')
    if args_parse.prefix is None:
        args_parse.prefix = args_parse.trj.split('.')[0]

    return args_parse


if __name__ == '__main__':

    args = initialize()

    t, CV = [], []
    infile = open('%s' % args.CVfile, 'r')
    lines = infile.readlines()
    #infile.close
    # Parse data
    m = 0
    for line in lines:
        if line[0] == '#' or line[0] == '@':
            m += 1
    for line in lines[m:]:
        if line[0] != '#' and line[0] != '@':
            tokens = line.split()
            t.append(float(tokens[0]))
            CV.append(float(tokens[1]))
    t, CV = np.array(t), np.array(CV)

    # defult of time: output the file at the time frame that CV=max
    if args.time is None:
        args.time = t[list(CV).index(max(CV))]
        print(max(CV))

    if args.mpi:
        os.system("gmx_mpi trjconv -f %s -s %s -o %s_%sps.pdb -dump %s " %
                  (args.trj, args.tpr, args.prefix, args.time, args.time))

    if not args.mpi:
        os.system("gmx trjconv -f %s -s %s -o %s_%.0gps.pdb -dump %s " %
                  (args.trj, args.tpr, args.prefix, args.time, args.time))
