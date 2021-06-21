import argparse
import os
import csv
import regex as re
import sys
import pandas as pd

function_description = "Converts .csv into .xlsx"
working_directory = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description=function_description)
parser.add_argument('-CSV', nargs='?', help=".csv file to be converted", required=True)

args = parser.parse_args()

csvfile = args.CSV
#excelname = csv[:-4] + ".xlsx"
linelist = []
firstline = []
tmp_csv = csvfile[:-4] + "_tmp.csv"
tmpfile = csvfile[:-4] + "_copy.csv"
excelname = "EXCEL_" + csvfile[:-4] + ".xlsx"

with open(csvfile, 'r') as initial, open(tmpfile, 'w') as tempfile:
	for line in initial:
		tempfile.write(line)
copyfile = open(tmpfile, 'r')
filecontents = copyfile.readlines()

with open(csvfile, 'r') as csv_file:
	with open(tmp_csv, 'w') as temp_csv:
		csvwriter = csv.writer(temp_csv)
		count = 0 #maybe goes outside for loop here
		for id, line in enumerate(csv_file):
			if count > 0:
				count -= 1
				continue
			if id == 0:
				line = line.split(',')
				for id, i in enumerate(line):
					line[id] = i.replace('"', '').replace('\n', '').replace('\r', '')
				firstline = line	
				csvwriter.writerow(line)
				continue
			if not line:
				continue
			while not (line.startswith('"') and line.endswith('"""\n')):
				try:
					if line[-2:] == ';\n':
						#print(line[-2])
						#print(repr(line[-1:]))
						#print(repr(line[:-2] + '\n'))
						line = line[:-2] + '\n'
						continue
				except IndexError:
					pass
				#print(repr(line))
				line = line[:-2]
				#print(line + '\n')
				line = line + filecontents[id + count + 1]
				count += 1
				linelist.append(line)
				#print(line)

				#print(linelist)
			line = line[0:-4]
			line_match = re.search(r'^("\d*)', line, flags=re.MULTILINE)
			startingnumber = line_match.group(1)
			matchlength = len(startingnumber)
			line = line[matchlength:]
			newstartnumber = startingnumber[1:] + '""'
			line = newstartnumber + line
			#linelist.append(line)
			csvline = line.split('"",""')
			if len(csvline) != len(firstline):
				print("ERROR in line creation")
				print(line)
				sys.exit()
			csvwriter.writerow(csvline)
			#print("iteration completed")

copyfile.close()

dataframe = pd.read_csv(tmp_csv)
excel = pd.ExcelWriter(excelname)
dataframe.to_excel(excel, index = False)
excel.save()