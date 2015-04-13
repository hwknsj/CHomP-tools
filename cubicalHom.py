import subprocess
import time
import os
import signal
import multiprocessing as mp
import sys
from sys import version_info

print "Homology batch script. Runs 'chomp-cubical' on each file in the input folder outputs to file with name of first file.\n"

# Input should be of the form "python batchHomGridTest.py infolder outfolder"

py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

if len(sys.argv) < 3:

	if py3:
		in_folder = input("Input folder for txt files?")
		if not os.path.exists(in_folder):
			in_folder = input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")
	  
	else:
		in_folder = raw_input("Input folder? (e.g. 'plots or 'files/imgs'): ")
		if not os.path.exists(in_folder):
			in_folder = raw_input("That folder doesn't exist. Input folder? (e.g. 'plots'): ")

else:
	in_folder = sys.argv[1]
	out_folder = sys.argv[2]

if not os.path.exists(out_folder):
		os.makedirs(out_folder)

def makeSubfolderList(in_folder):
	subfolders = os.listdir(in_folder)
	subfolders.sort()
	if '.DS_Store' in subfolders:
		subfolders.remove('.DS_Store')
	return subfolders

def fileExists(resultsName):
	if os.path.isfile(resultsName):
		existing = open(resultsName)
		linect = 0
		for line in existing:
			linect += 1
		existing.close()
		if linect >= 2500:
			return True
		else:
			return False
	else:
		return False

def batchHomGrid(subfolders,in_folder):
	folderct = 1
	for folder in subfolders:
		files = os.listdir('./'+in_folder+'/'+folder)
		if '.DS_Store' in files:
			files.remove('.DS_Store')

		files = sorted(files) # make sure the list is sorted!

		resultsName = out_folder + '/' + folder + ".csv"
		if fileExists(resultsName):
			print resultsName + " already exists! Skipping...\n"
		else:
			print "Analyzing homology of folder " + folder + " ("+str(folderct)+" of " + str(len(subfolders))+ ")\n"
			subprocess.call(["touch",resultsName])
			print resultsName + " file created. \n"
			count = 1
			resultsFile = open(resultsName, 'r+')
			resultsFile.write('name-step,betti-0,betti-1,betti-2 \n')

			for file in files:
				p = subprocess.Popen(["chomp-cubical","./"+in_folder+"/"+folder+"/"+file], stdout=subprocess.PIPE)
				output, err = p.communicate()
				# want to print csv: STEP,b0,b1,b2
				# where STEP is the time step e.g. 004 or 326 (3 digits, out of 500 steps, could be more)
				# chomp-cubical gives e.g. 'Betti Numbers: 5 16 0'
				bettis = output.split()[-3: ] # gets ['5', '16', '0']
				bettisStr = bettis[0]+','+bettis[1]+','+bettis[2]
				# file is the input filename, e.g. 'theta-491.png.txt'
				tStep = file.split('.')[0] # 'theta-491'
				sys.stdout.write("\r Processing " + str(count) + " of " + str(len(files)) + " | " + tStep + ': ' + bettisStr)
				sys.stdout.flush()
				count += 1
				resultsFile.write(tStep + ',' + bettisStr + '\n')

			resultsFile.write('\n')
			resultsFile.close()
			sys.stdout.write("\n")
			print "Results saved in " + resultsName + "\n"
			folderct += 1

	print "All done."


f = makeSubfolderList(in_folder)
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
processes = [mp.Process(target=batchHomGrid, args=(fi,in_folder)) for fi in foffs]

# run each process
for p in processes:
	p.start()

# exit each process
for p in processes:
	p.join()
