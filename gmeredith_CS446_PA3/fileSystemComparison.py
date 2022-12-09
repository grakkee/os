#Grace Meredith
#CS446 PA3 ~ Create & Compare/Contrast a single level directory & hierarchical directory
#Due: 10 April 2022

'''

Q1: There are a few differences in the output between the single level system & the hierarchical system.
	First, Hierarchical shows to have 110 files rather than 100. This is because it has an additional 10 directories
	to account for. Second, the average file size in hierarchical is larger than the file size average in singel level.
	This is because the included directories each hold 10 files so they are considered to have more memory. Finally,
	the hierarchial traversal time is longer than the single level. This is because each branch from the root of hierarchical
	contains a sub-tree of directory and files making it longer to Traverse. The height of the single level tree is shorter, as
	it only has one root with many children, so the traversal time is slightly shorter.

Q2: If arbitrarily long names can be used then it is possible to simulate a multilevel directory structure. This can be done, 
	for example, by using the character “.” to indicate the end of a subdirectory. Thus, for example, the name jim.java.F1 
	specifies that F1 is a file in subdirectory java which in turn is in the root directory jim. 

'''

import os
import time

def setRoot(directory):
	os.mkdir(directory)

def setSingleFiles(singlePath):
	n = 1
	while n <= 100:
		newFile = "file" + str(n) + ".txt"
		newPath = os.path.join(singlePath, newFile)
		file1 = open(newPath, "w")
		file1.close()
		n = n + 1

def setHierFiles(hierPath):
	f = 1
	l = 10
	while l <= 100:
		newDirectory = "files" + str(f) + "-" + str(l)
		newPath = os.path.join(hierPath, newDirectory)
		os.mkdir(newPath)
		for x in range(f,l+1):
			newFile = "file" + str(x) + ".txt"
			newPath2 = os.path.join(newPath, newFile)
			file1 = open(newPath2, "w")
			file1.close()
		f = f+10
		l = l+10

def traverse(path):
	Dict = {}
	startTime = time.time()
	for root, dirs, files in os.walk(path, topdown=True):
		if len(dirs) > 0:
			for x in dirs:
				newPath = os.path.join(path, x)
				Dict.update({x: os.path.getsize(newPath)})	
		else:
			for x in files:
				Dict.update({x: os.path.getsize(os.path.join(root, x))})
	endTime = time.time()
	return Dict,(endTime - startTime)*1000

def writeResults(newFile, Dict):
	f0 = open(newFile, "w")
	for item in Dict.items():
		f0.write(str(item))
	f0.close()

def findAVG(Dict):
	n = 0
	avg = 0
	for value in Dict.values():
		avg += int(value)
		n = n+1
	avg = avg/n
	return n,avg

def main():
	singlePath = "singleRoot"
	hierPath = "hierarchicalRoot" 

	setRoot(hierPath)
	setRoot(singlePath)

	setSingleFiles(singlePath)
	setHierFiles(hierPath)

	singleDict, singleTime = traverse(singlePath)
	sNumFiles, sAverage = findAVG(singleDict)

	hierDict, hierTime = traverse(hierPath)
	hNumFiles, hAverage = findAVG(hierDict)

	writeResults("singleLevelFiles.txt", singleDict)
	writeResults("hierarchicalFiles.txt", hierDict)

	print("Single Level File System", "\nNumber of Files: ", sNumFiles, "\nAverage File Size: ", sAverage, "\nTraversal Time: ", singleTime)
	print("\nHierarchical File System", "\nNumber of Files: ", hNumFiles, "\nAverage File Size: ", hAverage, "\nTraversal Time: ", hierTime)



if __name__ == "__main__":
	main()