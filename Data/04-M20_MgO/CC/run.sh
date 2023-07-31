#!/bin/bash

set -e

for i in 3 #1 2
do
        for j in 1 3 # 2 3
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
                cp ../../Input/MINP_Au20_${i}_PBE_${j} MINP_PBE
                cp ../../Input/MINP_Au20_${i}_LNOCC_${j} MINP_CC
                cp ../../bose_mrcc.sh .
                qsub ./bose_mrcc.sh
                cd ../../
        done
done

