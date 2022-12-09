#CS446 Assignment 1 Part 1
#Grace Meredith
#4 March 2022

fout = open("gmeredith_systemDetails.txt", "a")

#CPU type & model, Kernal version
#found in /proc/version
with open("/proc/version", "r") as f:
	CPUType = f.readlines()
count = 0
for line in CPUType:
	count += 1
	fout.write(f'CPU type, model & Kernal details: {line}')
fout.write("\n")

#Amount of time passed since last system boot
#found in /proc/uptime
with open("/proc/uptime", "r") as f:
	TimeSinceBoot = f.readlines()
count = 0
for line in TimeSinceBoot:
	count +=1
	fout.write(f'Amount of time since last boot: {line}')
fout.write("\n")

#Time of last system boot & number of processes
#found in /proc/stat
with open("/proc/stat", "r") as f:
	TimeOfBoot = f.readlines()
count = 0
for line in TimeOfBoot:
	count +=1
	if count == 12:
		fout.write(f'Time of last system boot: {line}')
	if count == 13:
		fout.write(f'Number of Processes: {line}')
fout.write("\n")

#Number of disk requests
#found in /proc/diskstats
fout.write("Disk Stats: ")
with open("/proc/diskstats", "r") as f:
	NumDisks = f.readlines()
count = 0
for line in NumDisks:
	count +=1
	fout.write(f'{line}')
	
fout.close()