#!/bin/bash

vaspinputs="/scratch/x2555a01/au20/inputs_au"
poscars="/scratch/x2555a01/au20/rev-vdW-DF2-m20opt"
element="Au20"

for i in 1 
do
for xc in pbe pbe-d2 pbe-d2-ne pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi pbe-mbdfi pbesol pbesol-d3 pbesol-d4 revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 m06l r2scan r2scan-d3 r2scan-d4 scan-rvv10 
do
for sys in AD
do
rm -rf ${i}/${xc}/${sys}
mkdir -p ${i}/${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i}_${sys} ${i}/${xc}/${sys}/POSCAR
cp mpi.sh ${i}/${xc}/${sys}
cd ${i}/${xc}/${sys}
sed -i 's/KPAR=2/KPAR=1/' INCAR
qsub mpi.sh
cd ../../../
done
done
done
