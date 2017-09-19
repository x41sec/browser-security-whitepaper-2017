#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import csv

inputs = ['/home/eric/arbeit/google-browser/browser2/Data/History/chrome.csv', '/home/eric/arbeit/google-browser/browser2/Data/History/edge.csv', '/home/eric/arbeit/google-browser/browser2/Data/History/ie.csv']
names = ['Chrome', ' Edge', 'IE']
my_colors = ['#d04b3e', '#0078d7', '#1ebbee']  #red, green, blue, black, etc.
result = []

for f in inputs:
	with open(f, 'rb') as csvfile:
		input = csv.DictReader(csvfile, delimiter=';')
		days = []
		for row in input:
			rep = pd.to_datetime(row["reported"])
			rel = pd.to_datetime(row["released"])
			diff = rel - rep
			days.append(diff.days)

		# geometric mean
		mean = int(reduce(lambda x, y: x*y, days)**(1.0/len(days)))
		result.append(mean)
		print f
		print days
		print mean

s = pd.Series(
    result,
    index = names
)

#Set descriptions:
plt.ylabel('Days to Fix')

#Set tick colors:
ax = plt.gca()

s.plot(
    kind='bar', 
    color=my_colors,
)

#plt.show()
plt.tight_layout()
plt.savefig("browser_days_to_fix.png", dpi=300)

print result
