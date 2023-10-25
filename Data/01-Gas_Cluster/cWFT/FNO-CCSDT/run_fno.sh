#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 6 #4
	do
		for k in 1 2 3 4
		do
			for l in 2
			do
				mkdir -p ${i}${j}/FNOCC/${k}/${l}
				cd ${i}${j}/FNOCC/${k}/${l}
				if [ ${l} = 2 ]; then
					cp ../../../../Input_Files/MINP_${i}${j}_${k}_PBE0_3_Restart MINP_PBE0
				else
					cp ../../../../Input_Files/MINP_${i}${j}_${k}_PBE0_${l}_Restart MINP_PBE0
				fi
				cp ../../../../Input_Files/MINP_${i}${j}_${k}_FNOCC_${l} MINP_CC
				cp ../../../../cirrus_mrcc_long.sh .
				sbatch cirrus_mrcc_long.sh
				cd ../../../../
			done
		done
	done
done
