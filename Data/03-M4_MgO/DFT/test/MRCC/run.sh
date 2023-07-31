#!/bin/bash

set -e

for i in Au #Ag Cu
do
	for j in 4 # 6 8
	do
		for k in 1 2 3 4
		do
				mkdir -p ${i}${j}/${k}/
				cd ${i}${j}/${k}/
				cp ../../Data/MINP_${i}${j}_${k}_PBE MINP
				cp ../../cirrus_mrcc.sh .
				sbatch cirrus_mrcc.sh
				cd ../../
		done
	done
done
