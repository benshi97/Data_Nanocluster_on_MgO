#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 4 6 8
	do
		for k in 1 2 3 4
		do
			for l in 1 2 # 3
			do
				mkdir -p ${i}${j}/${k}/${l}
				cd ${i}${j}/${k}/${l}
				cp ../../../Input_Files/MINP_${i}${j}_${k}_FNOCC_${l} MINP
				cp ../../../cirrus_mrcc.sh .
				sbatch cirrus_mrcc.sh
				cd ../../../
			done
		done
	done
done
