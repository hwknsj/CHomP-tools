# csvSplit.py by Joel Hawkins
# hwknsj@gmail.com, hwknsj@github
#
# Just a faster way to split CSV files
# syntax: python csvSplit.py file.csv column line_start line_end outfilename.csv
# or using function: splitcsv('file.csv', column, start, end)

import os
import csv
import sys

def splitcsv(csvfile, column, outfile):
	subprocess.call(["touch",outfile])
	out = open(outfile, 'r+')
	with open(csvfile, 'rU') as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			out.write(row[column] + '\n')
		out.close()
	file.close()
	return out
	
def splitcsvRange(csvfile, colst, colend, rowstart, rowend='end', outfile='output'):
	outArr = []
	with open(csvfile, 'rU') as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			outArr.append(row[colst:colend])
	file.close()
	subprocess.call(["touch",outfile])
	if rowend == 'end':
		rowend = len(outArr)
	out = open(outfile, 'r+')
	for i in range(rowstart,rowend):
		for j in range(len(outArr[i])):
			if j == len(outArr[i]) - 1:
				out.write(outArr[i][j])
			else:
				out.write(outArr[i][j] + ',')
		out.write('\n')
	out.close()
	return out

def cutcolscsv(csvfile,colend,outfile='output'):
	splitcsvRange(csvfile,0,colend,0,'end',outfile)

names = ['alpha','beta','delta','epsilon','eta','gamma','iota','kappa','lambda','mu','theta','zeta']

def splithists(names):
	for x in names:
		filename = x + '144_bbhist.csv'
		outbb = x + '_state.csv'
		# grab state b0,b1
		splitcsvRange(filename, 0, 2, 1, 'end', outbb)
		# grab Pi
		outPi = x + '_pi.csv'
		splitcsvRange(filename, 2, 3, 1, 'end', outPi)
