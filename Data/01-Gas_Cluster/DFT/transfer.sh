#!/bin/bash

set -e

for i in Au Ag Cu
do
	a=$(echo ${i} | awk '{print tolower($0)}')
	for j in 4 6 8
	do
		mkdir -p ${i}${j}

		cp -r /zfs/am452/share/2021_Nanocluster/03-DFT_Benchmarks/gasphase/${a}${j}/dft/* ${i}${j}
	done
done
