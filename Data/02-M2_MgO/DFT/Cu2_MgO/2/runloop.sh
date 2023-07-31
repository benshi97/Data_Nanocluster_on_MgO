#!/bin/bash
vaspinputs="/work/e89/e89/cwm31/03-DFT_Benchmarks/cu2/inputs_cu"
poscars="/work/e89/e89/cwm31/03-DFT_Benchmarks/rev-vdW-DF2"
element="Cu"

#for xc in pbe pbe-d2 pbe-d2-ne pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 r2scan-d4 scan-rvv10 b3lyp-d2 b3lyp-d2-ne b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06-d4
i=2
for xc in pbe-mbdfi b3lyp hse06  
do
for sys in AD SLAB AD_SLAB #AD SLAB
do
rm -rf ${xc}/${sys}
mkdir -p ${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${xc}/${sys}
cp archer_vasp.sh ${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i}_${sys} ${xc}/${sys}/POSCAR
cd ${xc}/${sys}
##echo "SYMPREC=1E-10" >> INCAR
sbatch archer_vasp.sh

cd ../../
done
done
