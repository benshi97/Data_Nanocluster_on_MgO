#!/bin/bash

set -e


for i in Au Ag Cu #  #Ag Cu
do
	for j in {1..4}  #1 #{1..6} #{1..8}
	do
		for k in {1..8} # {1..8}
		do
			for l in LMP2_normal LMP2_tight DFMP2
			do
				if [ ${l} == LMP2_normal ]; then
					a="${i}_LMP2_tetramer_${j}_rdf_${k}_1_MINP"
				elif [ ${l} == LMP2_tight ]; then
					a="${i}_LMP2_tetramer_${j}_rdf_${k}_3_MINP"
				elif [ ${l} == DFMP2 ]; then
					a="${i}_DFMP2_tetramer_${j}_rdf_${k}_3_MINP"
				fi

				#echo "${l} ${a}" #${i} $
				for m in AD_SLAB  #SLAB_CP AD_CP
				do
					mkdir -p ${i}/${j}/${k}/${l}/${m}
					cd ${i}/${j}/${k}/${l}/${m}

					cp ../../../../../Input/${a}_${m} MINP
					cp ../../../../../cirrus_mrcc.sh .
					sbatch cirrus_mrcc.sh
					cd ../../../../../
				done
			done
		done
	done
done


