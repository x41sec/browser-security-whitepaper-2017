#!/bin/bash
#simple grep ZDI information into a CSV file
out="edge.csv"

echo "Name;reported;released" > $out

for a in ZDI*; do 
	contact=`egrep ^201.- $a | grep reported | cut -d " " -f 1`; 
	release=`egrep ^201.- $a | grep Coordina | cut -d " " -f 1`;  
	echo "$a;$contact;$release"; 
done >> $out

