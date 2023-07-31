#!/bin/bash
vaspinputs="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/au4/dft/inputs_au_gas"
poscars="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/au4/optstr"
element="au4"

for i in 1 2 3 4 #5 6 7 8
do
#for xc in pbe pbe-d2 pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 r2scan-d4 scan-rvv10 b3lyp-d2 b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06-d4
#for xc in pbesol pbesol-d3 pbesol-d4 r2scan r2scan-d3 m06l
for xc in pbe-mbdfi pbe0-mbdhi pbe0-mbdfi b3lyp hse06
do
for sys in AD #AD_SLAB #AD SLAB
do
rm -rf ${i}/${xc}/${sys}
mkdir -p ${i}/${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${i}/${xc}/${sys}
cp archer_vasp.sh ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i} ${i}/${xc}/${sys}/POSCAR
cd ${i}/${xc}/${sys}
##echo "SYMPREC=1E-10" >> INCAR
sbatch archer_vasp.sh

cd ../../../
done
done
done
