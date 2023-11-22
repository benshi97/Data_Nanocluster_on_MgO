#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 1 2 3 4
	do
		for k in 1 2 3
		do
			mkdir -p ${i}/${j}/${k}
			cd ${i}/${j}/${k}
			if grep -Fq "Normal termination of mrcc" mrcc.out; then
				echo "${i}/${j}/${k} finished"
			else
				echo "${i}/${j}/${k} NOT FINISHED"
			fi
			cd ../../../
		done
	done
done
