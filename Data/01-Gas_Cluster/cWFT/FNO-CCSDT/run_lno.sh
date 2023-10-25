#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 6 #4
	do
		for k in 1 2 3 4
		do
			for l in 1 2 3
			do
				mkdir -p ${i}${j}/LNOCC/${k}/${l}
				cd ${i}${j}/LNOCC/${k}/${l}
				cp ../../../../Input_Files/MINP_${i}${j}_${k}_PBE0_${l}_Restart MINP_PBE0
				cp ../../../../Input_Files/MINP_${i}${j}_${k}_${l}_Restart MINP_CC
				cp ../../../../cirrus_mrcc.sh .
				sbatch cirrus_mrcc.sh
				cd ../../../../
			done
		done
	done
done
