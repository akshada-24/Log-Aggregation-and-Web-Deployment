import pandas as pd
import os
  

def f1(log_name, log_date, log_keyword,s3Buc):
	print("Inside samelog_function\n")
	print("log_name, log_date, log_keyword received")
	s3Buc.download_file(Key='Dates/{}/system/{}'.format(log_date,log_name),Filename='temp.csv')
	df1=pd.read_csv('temp.csv',sep="\n",header=None)
	#print(df1.head())   # prints few lines
	col1=[]
	col2=[]
	for line in df1[0].str.split(": "):
		#print(line)
		col1.append(line[0])
		col2.append(line[1])
		#col3.append(line[2])
		#col4.append(line[3])
	dict1={'data':col1, 'Message':col2}
	df2=pd.DataFrame(dict1)
	#print(df2) 
	print("---"*30)
	Date=[]
	Time=[]
	for line in df2['data'].str.split("T"):
		Date.append(line[0])
		Time.append(line[1])
		#owner.append(line[2])
		#system.append(line[3])
	dict2={'Date':Date,'Time':Time}
	#print(pd.DataFrame(dict2))
	df3=pd.concat([pd.DataFrame(dict2),df2['Message']],axis=1)      #concatinating message column
	#print(df3)
	time=[]
	owner=[]
	system=[]
	for line in df3['Time'].str.split(" "):
		time.append(line[0])
		owner.append(line[1])
		system.append(line[2])
	dict3={'Time':time, 'Owner':owner, 'System':system}
	df4=pd.concat([ df3['Date'],pd.DataFrame(dict3), df2['Message']],axis=1)
	print(df4)	
	
	list_index=[]
	import time
	temp=log_keyword
	t1=time.time()
	for row in df4.iterrows():
		if temp in row[1][-1]:
			list_index.append(row[0])
	t2=time.time()
	print("Total time:",t2-t1)
	name=input("Please enter the file name for storing the output with .csv extention:")
	df4.loc[list_index,:].to_csv(name,sep="\t")

#temp=input("Enter the name of the log file:")
#temp="systemd.log"
#f1(log_name, log_date, log_keyword)