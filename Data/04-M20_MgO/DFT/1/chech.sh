#!/bin/bash

for i in 1 
do
for xc in pbe-mbd pbe-mbdhi pbe-mbdfi pbesol pbesol-d3 pbesol-d4 revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 m06l r2scan r2scan-d3 r2scan-d4 scan-rvv10 
do
for sys in AD_SLAB
do
echo $xc
tail -2 ${xc}/${sys}/log
done
done
done
