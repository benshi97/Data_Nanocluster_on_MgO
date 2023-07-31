#!/bin/bash

vaspinputs="/scratch/x2555a01/au20/inputs_au"
poscars="/scratch/x2555a01/au20/rev-vdW-DF2-m20opt"
element="Au20"

for i in 3 
do
for xc in pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi pbe-mbdfi pbesol-d4 revpbe-tshi revpbe-d4 r2scan-d4
do
for sys in AD_SLAB
do
rm -rf ${i}/${xc}/${sys}
mkdir -p ${i}/${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i}_${sys} ${i}/${xc}/${sys}/POSCAR
cp mpi.sh ${i}/${xc}/${sys}
cd ${i}/${xc}/${sys}
qsub mpi.sh
cd ../../../
done
done
done
