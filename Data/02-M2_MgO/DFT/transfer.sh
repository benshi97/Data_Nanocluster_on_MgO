#!/bin/bash

set -e

for i in Au Ag Cu
do
	a=$(echo ${i} | awk '{print tolower($0)}')
	for j in 2 # 4 6 8
	do
		mkdir -p ${i}${j}_MgO
		cp -r /zfs/am452/share/2021_Nanocluster/03-DFT_Benchmarks/${a}${j}/{1..8} ${i}${j}_MgO
	done
done
