# entropy.py by Joel Hawkins
# hwknsj@gmail.com, hwknsj@github
#
# Calculates the Shannon entropy S given a .csv with step and
# Betti number information formatted like so:
# name-step, b0, b1
#
# use saveEntropyCSV to write out a CSV of entropies given a folder of
# CSVs containing Betti numbers for each time step (i.e. the output of cubicalHom.py) 
# 
# Returns a CSV with the following information
# F, k, S where F, k are given in the Gray-Scott equation
# (this method obtains these from the folder name)

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import csv
import sys

def entropy(P_i):
	S = 0.0
	for i in P_i:
		S += -(i*np.log(i))
	return S

def bettiList(csvfile):
	betti = []
	with open(csvfile, 'rU') as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			b0b1 = row[1: 3] # convert the b0, b1 part to a string like '[b0 b1]'
			b0b1str = ','.join(b0b1)
			betti.append(b0b1str)
	file.close()
	return betti

def makeP_i(csvfile):
	betti = bettiList(csvfile)
	N = len(betti)
	hist = Counter(betti).items()
	hist.sort(lambda x, y: cmp(x[1], y[1]), reverse=True) # largest vals first
	P_i = np.array([np.divide(pair[1], N, dtype=np.float) for pair in hist])
	return P_i, hist, N

def saveEntropyCSV(infolder,outfile):
	filelist = os.listdir(infolder)
	if '.DS_Store' in filelist:
			filelist.remove('.DS_Store')
	subprocess.call(['touch',outfile])
	csv = open(outfile, 'r+')
	for csvfile in filelist:
		P_i = makeP_i( infolder + '/' + csvfile )[0]
		S = entropy(P_i)
		F = csvfile.split('_')[0] # e.g. '0.044_0.038.csv'
		k = csvfile.split('_')[1][ :-4] #remove '.csv'
		csv.write( F + ',' + k + ',' + str(S) + '\n')
	csv.close()

def makeHist(csvfile):
	P_i, hist, N = makeP_i(csvfile)

	Ni = np.array(hist)

	S = entropy(P_i)

	# normalize Ni
	for pair in Ni:
		pair[1] = np.divide(pair[1],N,dtype=np.float)

	print Ni[0], Ni[1]

	outfile = sys.argv[1][ :-4]+'hist.csv' # file[ :-4] removes '.png'
	#outfile = outfile[ :-4]+'hist.csv' # file[ :-4] removes '.png'
	subprocess.call(["touch",outfile])

	out = open(outfile, 'r+')
	out.write('b0,b1,P_i, S='+S.astype('|S10')+'\n')
	
	for i in range(len(Ni)):
		out.write(Ni[i][0]+','+P_i[i].astype('|S10')+'\n') # Ni[i][0] is "b0,b1"

	out.write('\n')
	out.close()
	print "Probability information saved in " + outfile

	print "The entropy of this system is S = " + str(S)
