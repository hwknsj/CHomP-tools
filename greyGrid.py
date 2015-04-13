# greyGrid.py by Joel Hawkins
# hwknsj@gmail.com, hwknsj@github
#
# The syntax for greyGrid.py is
# python greyGrid.py input_folder threshold output_folder
#
# This batch converts an entire folder containing many subfolders of images (png, jpg etc.)
# to 2-bit binary images thresholded. It utilizes CHomP, written by Shaun Harker.

import subprocess
import os
import multiprocessing as mp
import sys
from sys import version_info

print "Batch greyscale conversion. Uses 'chomp-greyscale-to-cubical' to convert all files in a folder.\n"

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

if len(sys.argv) < 4:

	if py3:
		in_folder = input("Input folder? (e.g. 'plots' or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_folder = input("Where to output? (e.g. 'out') ")
		threshold = input("Threshold: ")
	  
	else:
		in_folder = raw_input("Input folder? (e.g. 'plots or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = raw_input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
		out_folder = raw_input("Where to output? (e.g. 'out') ")
		threshold = raw_input("Threshold: ")

else:
	in_folder = sys.argv[1]
	threshold = sys.argv[2]
	out_folder = sys.argv[3]

def removeDS(folder):
	if '.DS_Store' in folder:
		folder.remove('.DS_Store')

def batchGrey(subfolders, in_folder, threshold, out_folder):
	out_folder = out_folder + "_" + str(threshold) # add threshold so i dont forget
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
	print "Converting to greyscale...\n"
	for folder in subfolders:
		count = 1
		files = os.listdir('./'+in_folder+'/'+folder)
		removeDS(files)

		if not os.path.exists(out_folder+'/'+folder):
			    os.makedirs(out_folder+'/'+folder)

		print 'Working in ' + folder + "\n"
		for file in files:
			infile = "./"+in_folder+"/"+folder+"/"+file
			outfile = "./"+out_folder+"/"+folder+"/"+file[ :-4]+".txt" # file[ :-4] removes '.png'

			p = subprocess.call(["chomp-greyscale-to-cubical", infile, str(threshold), outfile])

			sys.stdout.write("\r Processing " + str(count) + " of " + str(len(files)) )
			sys.stdout.flush()

			count += 1
	print "Done.\n"

subfolders = os.listdir(in_folder)
removeDS(subfolders)

subfolders.sort() 

# split into 8 lists for parallel computation
f = subfolders

l8 = len(f)/8
f0 = f[:l8]
f1 = f[l8:l8*2]
f2 = f[l8*2:l8*3]
f3 = f[l8*3:l8*4]
f4 = f[l8*4:l8*5]
f5 = f[l8*5:l8*6]
f6 = f[l8*6:l8*7]
f7 = f[l8*7: ]

# one list of all the split lists
foffs = [f0, f1, f2, f3, f4, f5, f6, f7]

# set up a list of processes to run
processes = [mp.Process(target=batchGrey, args=(fi,in_folder,threshold,out_folder,)) for fi in foffs]

# run each process
for p in processes:
	p.start()

# exit each process
for p in processes:
	p.join()
