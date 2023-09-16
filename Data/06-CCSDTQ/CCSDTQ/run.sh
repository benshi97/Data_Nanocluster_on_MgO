#!/bin/bash

set -e

for i in Au Ag Cu
do
    for j in 1 2 3 4
    do
        mkdir -p ${i}/${j}
        cd ${i}/${j}
        cp ../../MINP_LANL2DZ_${i}4_${j}_CCSDTQ MINP
        cp ../../young_mrcc.sh .
        qsub ./young_mrcc.sh
        cd ../../
        done
        done
