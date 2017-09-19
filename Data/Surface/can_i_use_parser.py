#!/usr/bin/python
import json
from pprint import pprint

with open('can_i_use_data_20170705.json') as data_file:    
    data = json.load(data_file)

data = data['data']
for key, value in data.iteritems():
	chrome = value['stats']['chrome']['59']
	edge = value['stats']['edge']['15']
	ie = value['stats']['ie']['11']

	if (chrome[:1] == 'a'):
		chrome = 'p'
	if (edge[:1] == 'a'):
		edge = 'p'
	if (ie[:1] == 'a'):
		ie = 'p'
	if (chrome[:1] == 'n'):
		chrome = 'n'
	if (edge[:1] == 'n'):
		edge = 'n'
	if (ie[:1] == 'n'):
		ie = 'n'
	if (chrome[:1] == 'y'):
		chrome = 'y'
	if (edge[:1] == 'y'):
		edge = 'y'
	if (ie[:1] == 'y'):
		ie = 'y'



	print "%s;%s;%s;%s" % (key, chrome, edge, ie)

#pprint(data)
