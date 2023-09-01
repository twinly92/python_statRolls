#a simple script to take arguments and roll six random stats for dnd

import random
import argparse
#we're gonna reinvent the wheel and implement our own dice function, because I like doing work that other people have already done
statArray=[0,0,0,0,0,0] #The array...of stats.. should be six items long
lowScoreTotal=72 #The lowest combined total that the stats can have, default 72
highScoreTotal=108 #The highest combined total the stats can have, default 108, statistically unlikely though
lowScore=18 #One score must be at or below this number, default to maximum score
highScore=18 #no score can be above this number (Default 18)
attempts=0#how many tries to meet the conditions
isValid=False#does the stat roll match the perameters

def getArgs():
	parser = argparse.ArgumentParser(description='Options for stat rolls')
	parser.add_argument('-lst','--lowScoreTotal', help='Sum of rolled stats must be above this number (from 0-108)', required=False)
	parser.add_argument('-hst','--highScoreTotal', help='Sum of rolled stats must be below this number (from 0-108)', required=False)
	parser.add_argument('-low','--lowScore', help='One stat must be below this number (3-18)', required=False)
	parser.add_argument('-high','--highScore', help='No stat can be above this number (3-18)', required=False)	
	args = vars(parser.parse_args())
	return(args)

#dice function
def dice(sides):
    return(random.randint(1,sides))

#a function to drop the lowest of four rolls
def dropLow(s1, s2, s3, s4):
	inRoll=[s1, s2, s3, s4]
	keeps=[]
	i=0
	while i < 3:
		keeps.append(max(inRoll))
		inRoll.remove(max(inRoll))
		i += 1
	return keeps

#roll 4d6 and drop the lowest stat, then add the remaining scores together and put those in each spot in the statArray
def ranStat():
	for y in range(len(statArray)):
		r1=dice(6)
		r2=dice(6)
		r3=dice(6)
		r4=dice(6)
		tRoll=dropLow(r1, r2, r3, r4)
		ns=0
		for i in range(len(tRoll)):
			ns +=tRoll[i]
		statArray[y]=ns


#check that the total is within the range assigned
def totalCheck():
	tot=sum(statArray)
	if lowScoreTotal < tot and highScoreTotal > tot:
		return True
	else:
		return False

#return true if at least one of the values is below the low number
def lowCheck():
	for i in range(len(statArray)):
		if statArray[i] < lowScore:
			return True		
	return False

#return true if any of the stats is above the high number
def highCheck():
	for i in range(len(statArray)):
		if statArray[i] > highScore:
			return True		
	return False

def readArgs(argIn):
	argDict={}
	if argIn["lowScoreTotal"] != None:
		argDict["lowScoreTotal"] = argIn["lowScoreTotal"]
	if argIn["highScoreTotal"] != None:
		argDict["highScoreTotal"] = argIn["highScoreTotal"]
	if argIn["lowScore"] != None:
		argDict["lowScore"] = argIn["lowScore"]
	if argIn["highScore"] != None:
		argDict["highScore"] = argIn["highScore"]	
	return(argDict)
	

#main loop. attempt until valid OR 100 attempts as a failsafe
#First, get any arguments
options=getArgs()
selectedOpts={}
selectedOpts=readArgs(options)
#print(selectedOpts)
if "lowScoreTotal" in selectedOpts:
	lowScoreTotal = int(selectedOpts["lowScoreTotal"])
	print("Sum of stats must be greater than: "+str(lowScoreTotal))
if "highScoreTotal" in selectedOpts:
	#print(selectedOpts["highScoreTotal"])
	highScoreTotal = int(selectedOpts["highScoreTotal"])
	print("Sum of stats must be less than: "+ str(highScoreTotal))
if "lowScore" in selectedOpts:
	lowScore = int(selectedOpts["lowScore"])
	print("At least one score must be below: "+str(lowScore))
if "highScore" in selectedOpts:
	highScore = int(selectedOpts["highScore"])
	print("No scores can be above: "+str(highScore))

while not isValid:# or attempts < 100:
	ranStat()
	low=lowCheck()
	high=highCheck()
	total=totalCheck()
	attempts +=1
	if attempts == 100:
		break
	if low and total and not high:
		isValid=True

print("Stats:")
print(statArray)
print("Stats Generated in: "+str(attempts)+" attempts.")
print("Actual Total: "+(str(sum(statArray))))