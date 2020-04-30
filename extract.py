import re
import pandas as pd
import numpy as np
from stateChange import *	

def extract_disease_and_time(history, diseases_and_synonyms, row):
	# time_re = '((?:\bsince\b){0,1}[\s]+(([0-9]{1,2})[\s]+(year|month|yr|mo)[\(s\)|s]|childhood))'
	history = history.lower()
	print(history, row)
	diseases_re = f'({"|".join(diseases_and_synonyms)})\s'
	time_re = '(([0-9]{1,2})[\s]+(year|month|yr|mo|year|week))'
	no_re = 'no '

	pattern0 = re.compile(no_re,flags=re.IGNORECASE)
	pattern1 = re.compile(diseases_re,flags=re.IGNORECASE)
	pattern2 = re.compile(time_re,flags=re.IGNORECASE)
	ms = []
	curr_pos = 0
	curr_info = {"curr_state" : 0, "history": history, "row": row, "disease": None, "duration": None, "duration_unit": None}
	while(curr_pos<len(history)):
		# print("curr_pos : ", curr_pos)
		m = pattern0.match(history,curr_pos)
		if(m):
			print("Match found : ", m.group(0))
			curr_pos = m.end()
			ms, curr_info = makeTransition(ms, curr_info,'no', m.group(0))
			# print("curr_info : ", curr_info)
			continue
		m = pattern1.match(history,curr_pos)
		if(m):
			print("Match found : ", m.group(0))
			curr_pos = m.end()
			ms, curr_info = makeTransition(ms, curr_info,'disease', m.group(0))
			flag = 1
			# print("curr_info : ", curr_info)
			continue
		m = pattern2.match(history,curr_pos)
		if(m):
			print("Match found : ", m.group(0))
			curr_pos = m.end()
			ms, curr_info = makeTransition(ms, curr_info,'time',m.group(0))
			# print("curr_info : ", curr_info)
			continue
		curr_pos+=1	

	if curr_info["curr_state"] == 1 :
		ms.append(curr_info)
	print(curr_info)	
	print(ms)
	return ms



def save_excel(list_diseases,all_extracted):
	# all_extracted = all_extracted[0:15]
	df = pd.DataFrame(index=list_diseases)
	for extract in all_extracted:
		n_diseases = len(extract)
		if n_diseases > 0:
			a = np.zeros(len(list_diseases))
			temp = pd.Series(a,index=list_diseases)
			for info in extract:
				temp[info['disease'].strip()] = "exists"
				if(info['duration'] != None):
					temp[info['disease'].strip()] = info['duration']
			# print(temp)
			df[extract[0]['history']] = temp
	print(df.transpose())
	df = df.transpose()
	df.to_excel("output.xlsx")