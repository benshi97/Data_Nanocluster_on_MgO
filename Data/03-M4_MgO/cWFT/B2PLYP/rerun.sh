#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 1 2 3 4
	do
		for k in 1 #3
		do
			mkdir -p ${i}/${j}/${k}
			cd ${i}/${j}/${k}
			cp ../../../Input/${i}_LB2PLYP_Final_tetramer_${j}_rdf_6_${k}_MINP_AD_SLAB MINP
			a=$(ls | grep "mrcc.out" | tail -n 1  )
			b=${a: -7}
			cp ../../../cirrus_mrcc_${k}_restart.sh cirrus_mrcc.sh
			sed -i "s/INSERT_SLURM/${b}/g" cirrus_mrcc.sh 
			sed -i "s/scfiguess=small/lccrest=domain/g" MINP
			sbatch cirrus_mrcc.sh
			cd ../../../
		done
	done
done
