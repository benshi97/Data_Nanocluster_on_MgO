#!/bin/bash

vaspinputs="/scratch/x2555a01/au20/inputs_au"
poscars="/scratch/x2555a01/au20/rev-vdW-DF2-m20opt"
element="Au20"

for i in 1 2 3 
do
for xc in b3lyp b3lyp-d2 b3lyp-d2-ne b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06 hse06-d4  
do
for sys in AD_SLAB
do
rm -rf ${i}/${xc}/${sys}
mkdir -p ${i}/${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i}_${sys} ${i}/${xc}/${sys}/POSCAR
cp mpi-hf.sh ${i}/${xc}/${sys}
cd ${i}/${xc}/${sys}
sed -i 's/KPAR=2/KPAR=1/' INCAR
sed -i 's/ISYM=2/ISYM=3/' INCAR
sed -i 's/PREC=Accurate/PREC=Normal/' INCAR
sed -i 's/EDIFF=1E-6/EDIFF=1E-4/' INCAR
sed -i 's/NCORE=4/NCORE=16/' INCAR
qsub mpi-hf.sh
cd ../../../
done
done
done
