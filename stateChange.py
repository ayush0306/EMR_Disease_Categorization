import numpy as np

file_untimed = open("Logs/untimed.txt","w+")


def reset_info(row,history):
	return {"curr_state" : 0, "history": history, "row": row, "disease": None, "duration": None, "duration_unit": None}

def noAction(ms, action, info, text):
	print("No action to take")
	return ms, info

def untimedDisease(ms, action, info, diseaseName):
	print("Found an untimed disease %s at row %s" %(info["disease"],info["row"]), file=file_untimed)
	ms.append(info)
	info = reset_info(info["row"],info["history"])
	return foundDisease(ms, action, info, diseaseName)

def foundDisease(ms, action, info, diseaseName):
	print("Found the following disease : ", diseaseName)
	info["disease"] = diseaseName
	return ms, info

def timedDisease(ms, action, info, time):
	print("Had recognized a disease %s and now a time parameter %s" %(info["disease"],time))
	info["duration"] = time
	ms.append(info)
	info = reset_info(info["row"],info["history"])
	return ms, info

actionIndex = {"no": 0, "disease": 1, "time": 2}
transitionMatrix = np.zeros((3,3))
transitionAction = [[noAction for i in range(3)] for j in range(3)]
transitionAction[0][1] = foundDisease
transitionAction[1][2] = timedDisease
transitionAction[1][1] = untimedDisease

transitionMatrix = np.array([[2,1,0],[0,1,0],[0,0,0]])

def makeTransition(ms, curr_info, action, text):
	currState = curr_info["curr_state"]
	ms, curr_info = transitionAction[currState][actionIndex[action]](ms, action, curr_info, text)
	curr_info["curr_state"] = transitionMatrix[currState][actionIndex[action]]
	return ms, curr_info