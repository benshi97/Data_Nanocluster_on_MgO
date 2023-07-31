#!/bin/bash

for i in 1 
do
for xc in pbe pbe-d2 pbe-d2-ne pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi pbe-mbdfi pbesol pbesol-d3 pbesol-d4 revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 m06l r2scan r2scan-d3 r2scan-d4 scan-rvv10  b3lyp b3lyp-d2 b3lyp-d2-ne b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06 hse06-d4  
do
for sys in AD AD_SLAB
do
echo $i $xc $sys
tail -2 ${i}/${xc}/${sys}/log

done
done
done
