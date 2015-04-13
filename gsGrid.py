# gsGrid.py by Joel Hawkins
# hwknsj@gmail.com, hwknsj@github
#
# Requires gsLib.py
# Intended to run Gray-Scott simulations for a grid of F, k values


from gsLib import *
import multiprocessing as mp

"""
k will go from 0.03 to 0.07
F goes from 0.00 to 0.08
Always maintain relationship Du = 2*Dv

Make an array of lists: [Du, Dv, F, k, name]
Du = 0.16
Dv = 0.08

use np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
where "num" is the number of points to make in the range [start,stop]. if endpoint=true,
then stop is the last sample, otherwise it's like normal python
"""

def makeGrid(Du,Dv,Fstart,Fend,Fnum,kstart,kend,knum):
	dtype = np.float
	name = lambda f,k: f.astype('|S6') + '_' + k.astype('|S6')
	grid = [[Du, Dv, F, k, name(F,k)] for F in np.linspace(Fstart,Fend,Fnum,endpoint=True,retstep=False) for k in np.linspace(kstart,kend,knum,endpoint=False,retstep=False)]
	return grid

# Defaults, a 20x20 grid for F in [0.004, 0.08] and k in [0.03, 0.07]
Du, Dv, Fstart, Fend, Fnum, kstart, kend, knum = 0.16, 0.08, 0.004, 0.08, 20, 0.03, 0.07, 20

g = makeGrid(Du,Dv,Fstart,Fend,Fnum,kstart,kend,knum)

# split into lists for faster computation
l = len(g)
l8 = l/8

g0 = g[ :l8]
g1 = g[l8:l8*2]
g2 = g[l8*2:l8*3]
g3 = g[l8*3:l8*4]
g4 = g[l8*4:l8*5]
g5 = g[l8*5:l8*6]
g6 = g[l8*6:l8*7]
g7 = g[l8*7: ]

# one list of all the split lists
gofgs = [g0, g1, g2, g3, g4, g5, g6, g7]

def runGSList(list):
	for group in list:
		Du, Dv, F, k, name = group
		runGS(Du, Dv, F, k, name)

# set up a list of processes to run
processes = [mp.Process(target=runGSList, args=(gi,)) for gi in gofgs]

# run each process
for p in processes:
	p.start()

# exit each process
for p in processes:
	p.join()