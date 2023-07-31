#!/bin/bash
vaspinputs="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/ag4/dft/inputs_ag_gas"
poscars="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/ag4/optstr"
element="au2"

for i in 1 2 3 4 #3 #2 4 #5 6 7 8
do
#for xc in pbe pbe-d2 pbe-d2-ne pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 r2scan-d4 scan-rvv10 b3lyp-d2 b3lyp-d2-ne b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06-d4
#for xc in pbe pbe-d2 pbe-d2-ne pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 r2scan-d4 scan-rvv10 b3lyp-d2 b3lyp-d2-ne b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06-d4 pbesol pbesol-d3 pbesol-d4 r2scan r2scan-d3
for xc in b3lyp hse06 pbe pbe0-mbdfi pbe-d3 pbe-mbdfi pbesol-d4 r2scan-d3 revpbe-d4 scan-rvv10 b3lyp-d2 hse06-d4 pbe0 pbe0-mbdhi pbe-d4 pbe-mbdhi pbe-ts r2scan-d4 revpbe-ts vdw-df b3lyp-d3 m06l pbe0-d3 pbe0-tshi pbe-ddsc pbesol pbe-tshi revpbe revpbe-tshi vdw-df2 b3lyp-d4 optB86b-vdw pbe0-d4 pbe-d2 pbe-mbd pbesol-d3 r2scan revpbe-d3 rev-vdw-DF2
do
for sys in AD #SLAB #AD SLAB
do

echo $i $sys $xc 
#tail -1 $i/$xc/$sys/log  
grep LDIPOL $i/$xc/$sys/INCAR

done
done
done
