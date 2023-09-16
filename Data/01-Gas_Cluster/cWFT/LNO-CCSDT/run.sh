#!/bin/bash

set -e

for i in Cu # Au Ag Cu
do
	for j in 4 6 8
	do
		for k in 1 2 3 4
		do
			for l in 1 2 3
			do
				mkdir -p ${i}${j}/${k}/${l}
				cd ${i}${j}/${k}/${l}
				cp ../../../Data/MINP_${i}${j}_${k}_PBE0_${l}_Restart MINP
				cp ../../../Data/MINP_${i}${j}_${k}_${l}_Restart MINP_CCSDT
				cp ../../../cirrus_mrcc.sh .
				sbatch cirrus_mrcc.sh
				cd ../../../
			done
		done
	done
done
