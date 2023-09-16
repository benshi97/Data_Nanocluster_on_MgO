#!/bin/bash

set -e

for i in CCSDT #CCSDTQ #CCSDT CCSDTQ
do
        for j in Au #Ag # Cu
                do
                                for k in 1 2 3 4
                                                do
                                                                        mkdir -p ${i}/${j}_${k}
                                                                                                cd ${i}/${j}_${k}
                                                                                                                        cp ../../MINP_${j}4_${k}_${i} MINP
                                                                                                                                                sed -i 's/210GB/1500GB/g' MINP
                                                                                                                                                                        cp ../../young_mrcc.sh .
                                                                                                                                                                                               qsub ./young_mrcc.sh
                                                                                                                                                                                                                        cd ../../
                                                                                                                                                                                                                                        done
                                                                                                                                                                                                                                                done
                                                                                                                                                                                                                                                done

