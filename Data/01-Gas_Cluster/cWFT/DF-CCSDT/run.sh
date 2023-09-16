#!/bin/bash

set -e

for i in Au4 Ag4 Cu4
do
	for l in 1 2 3 4
	do
	if [ "${i}" != 'Au4' ] && [ "${l}" == 3 ]; then
                                continue
                                fi

	for j in DZ TZ QZ
	do
		for k in 0 1 2 3 4
		do
			mkdir -p ${i}/${l}/${j}/${k}
			cd ${i}/${l}/${j}/${k}
			cp ../../../../Input_Files/MINP_${i}_${l}_ACV${j}_mp2fit_${k} MINP
			cp ../../../../bose_mrcc.sh .
			qsub -N ${i}_${l}${j}${k} ./bose_mrcc.sh
			cd ../../../../
		done
	done
	done
done
		
