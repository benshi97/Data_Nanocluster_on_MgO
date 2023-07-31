#!/bin/bash

set -e

for i in 1 2 3
do
        for j in 1 2 3
        do
                mkdir -p ${i}_cheap/${j}
                cd ${i}_cheap/${j}
                cp ../../Input/MINP_Au20_${i}_PBE_cheap_${j} MINP_PBE
                cp ../../Input/MINP_Au20_${i}_LNOCC_cheap_${j} MINP_CC
                cp ../../bose_mrcc.sh .
                qsub ./bose_mrcc.sh
                cd ../../
        done
done

