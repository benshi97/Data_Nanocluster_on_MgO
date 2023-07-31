#!/bin/bash
vaspinputs="/work/e89/e89/cwm31/03-DFT_Benchmarks/au20/inputs_au"
poscars="/work/e89/e89/cwm31/03-DFT_Benchmarks/rev-vdW-DF2-m20opt"
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
cp archer_vasp.sh ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i}_${sys} ${i}/${xc}/${sys}/POSCAR
cd ${i}/${xc}/${sys}
sbatch archer_vasp.sh

cd ../../../
done
done
done
