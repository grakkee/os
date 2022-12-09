#Grace Meredith
#CS446 PA2 - Comparing Batch Scheduling Comparisons
#Due: 31 March 2022

"""
Priority Scheduling sorts processes by priority & arrival times, then schedules them accordingly
Shortest Job First sorts processes by Completion times & executes them accordingly
First Come First Served sorts processes by Arrival Times & executes them accordingly

First Come First Served:
◦Queue of ready processes
◦First job starts and runs
◦Other jobs enter queue
◦When running process is blocked, first ready queue 
runs
◦When process becomes unblocked, it goes to end of 
queue

Shortest Job First:
◦If jobs are equally important, the scheduler selects the shortest job; 
◦This allows multiple processes to finish in the time it might have taken one
◦Only optimal if alljobs are available at the same time.
◦Must know run time.

Priority:
◦Processes are not assumed to be of equal priority. 
Instead, provide the priority for each process and 
always run the one with the highest priority.

"""

import sys

def shortestJobFirstSort(batchFileData):
	#arrange arrival times
	n = len(batchFileData)
	for i in range(0, n):
		for j in range(i, n-i-1):
			if batchFileData[1][j] > batchFileData[1][j+1]:
				for k in range(0, n):
					batchFileData[k][j], batchFileData[k][j+1] = batchFileData[k][j+1], batchFileData[k][j]

    #completion times             
	value = 0
	batchFileData[3][0] = int(batchFileData[1][0]) + int(batchFileData[2][0])
	for i in range(1, n):
		temp = batchFileData[3][i-1]
		mini = batchFileData[2][i]
	for j in range(i, n):
		if temp >= batchFileData[1][j] and mini >= batchFileData[2][j]:
			mini = batchFileData[2][j]
			value = j
	batchFileData[3][value] = temp + batchFileData[2][value]
	for k in range(0, 4):
		batchFileData[k][value], batchFileData[k][i] = batchFileData[k][i], batchFileData[k][value]

	new_pid = [0] * len(batchFileData)
	for i in range(len(batchFileData)):
		new_pid[i] = batchFileData[i][0]

	return batchFileData[3], new_pid


def prioritySort(batchFileData):
	# declaring service array that stores
    # cumulative burst time
	batchFileData = sorted (batchFileData, key = lambda x:x[3])
	batchFileData = sorted (batchFileData, key = lambda x:x[1])
	service = [0] * len(batchFileData)
	wt = [0] * len(batchFileData)
 
    # Initialising initial elements
    # of the arrays
	service[0] = 0
	wt[0] = 0
 
	for i in range(1, len(batchFileData)):
		service[i] = int(batchFileData[i - 1][2]) + service[i - 1]
		wt[i] = service[i] - int(batchFileData[i][1]) + 1
 
        # If waiting time is negative,
        # change it o zero
		if(wt[i] < 0) :    
			wt[i] = 0

	new_pid = [0] * len(batchFileData)
	for i in range(len(batchFileData)):
		new_pid[i] = batchFileData[i][0]

	return wt, new_pid

def firstComeFirstServedSort(batchFileData):
	# waiting time for
    # first process is 0
	service_time = [0] * len(batchFileData)
	service_time[0] = 0
	wt = [0] * len(batchFileData)
	bt = [0] * len(batchFileData)
	for i in range(len(batchFileData)):
		bt[i] = int(batchFileData[2][i])
 
    # calculating waiting time
	for i in range(1, len(batchFileData)):
		service_time[i] = (service_time[i - 1] +
                                     bt[i - 1])
 
        # Find waiting time for current
        # process = sum - at[i]
		wt[i] = service_time[i] - int(batchFileData[i][1])
 
        # If waiting time for a process is in
        # negative that means it is already
        # in the ready queue before CPU becomes
        # idle so its waiting time is 0
		if (wt[i] < 0):
			wt[i] = 0
	new_pid = [0] * len(batchFileData)
	for i in range(len(batchFileData)):
		new_pid[i] = batchFileData[i][0]
		
	return wt, new_pid

def averageWait(wt):
	wavg = 0
	for i in range(len(wt)):
		wavg += int(wt[i])
	return wavg/len(wt)

def averageTurnaroundTimes(processCompletionTimes, processArrivalTimes):
	tavg = 0
	tat = [0] * len(processCompletionTimes)

	for i in range(len(processCompletionTimes)):
		tat[i] = int(processArrivalTimes[i]) + int(processCompletionTimes[i])

	for i in range(len(processCompletionTimes)):
		tavg += tat[i]
	return tat, tavg/len(processCompletionTimes)

def main(argv):
	if len(argv) != 3:
		print("Please Enter the Batchfile & Type of Sorting ALgorithm You Would Like to Use Along with the Executable.")
		sys.exit()
	else:
		#batchfile should contain PID, Arrival Time, Burst Time, Priority
		with open(argv[1]) as textFile:
			processes = [line.split() for line in textFile]
			#print(processes)
		for i in range(len(processes)):
			for j in range(4):
				processes[i][j] = processes[i][j].replace(",", "")

		processCompletionTimes = [0] * len(processes)
		newPIDs = [0] * len(processes)

		if argv[2] == "FIFO":
			processCompletionTimes, newPIDs = firstComeFirstServedSort(processes)
		elif argv[2] == "Priority":
			processCompletionTimes, newPIDs = prioritySort(processes)
		elif argv[2] == "ShortestFirst":
			processCompletionTimes, newPIDs = shortestJobFirstSort(processes) 
		else:
			print("Please Enter the Sorting Algorithm as one of the following: Priority, FIFO, ShortestFirst")
			sys.exit()

		processTurnaroundTimes, tavg = averageTurnaroundTimes(processCompletionTimes, processes[1])
		avgWait = averageWait(processCompletionTimes)

		print("New PID Order: ", newPIDs, "\nAverage Turn Around Time: ", tavg, "\nAverage Wait Time: ", avgWait)


if __name__ == "__main__":
	main(sys.argv)