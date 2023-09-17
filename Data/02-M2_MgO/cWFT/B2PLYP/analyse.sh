#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 1 2 3
	do
		for k in {1..8}
		do
			for l in AD_SLAB SLAB_CP AD_CP
			do
				cd ${i}/B2PLYP_${j}/${k}/${l}  
				grep "KOHN-SHAM ENERGY IN STEP" mrcc.out | tail -n 1
				cd ../../../../
			done
		done
	done
done
