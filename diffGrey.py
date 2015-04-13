# diffGrey.py by Joel Hawkins
# hwknsj@gmail.com, hwknsj@github
#
# Performs greyGrid.py for any missing images which are determined
# by examining the source folder
#
# syntax is: python diffGrey.py img_folder grey_folder threshold

import os
import sys
import multiprocessing as mp
import subprocess
import numpy as np

def removeDS(folder):
	if '.DS_Store' in folder:
		folder.remove('.DS_Store')

def batchGrey(subfolders,in_folder,threshold,out_folder):
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

		print 'Working in ' + folder
		for file in files:
			infile = "./"+in_folder+"/"+folder+"/"+file
			outfile = "./"+out_folder+"/"+folder+"/"+file[ :-4]+".txt" # file[ :-4] removes '.png'

			p = subprocess.call(["chomp-greyscale-to-cubical", infile, str(threshold), outfile])

			sys.stdout.write("\r Processing " + str(count) + " of " + str(len(files)) )
			sys.stdout.flush()

			count += 1
	print "Done.\n"

img_folder = sys.argv[1]
grey_folder = sys.argv[2]
threshold = sys.argv[3]
out_folder = sys.argv[4]

imglist = os.listdir(img_folder)
greylist = os.listdir(grey_folder)

imgset = set(imglist)
greyset = set(greylist)
diff = imgset.difference(greyset)
f = list(diff)

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
processes = [mp.Process(target=batchGrey, args=(fi,img_folder,threshold,out_folder,)) for fi in foffs]

# run each process
for p in processes:
	p.start()

# exit each process
for p in processes:
	p.join()
