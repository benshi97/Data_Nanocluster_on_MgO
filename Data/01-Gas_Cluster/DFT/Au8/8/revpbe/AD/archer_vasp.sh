#!/bin/bash

# Request 16 nodes (1024 MPI tasks at 64 tasks per node) for 3 hours
# Note setting --cpus-per-task=2 to distribute the MPI tasks evenly
# across the NUMA regions on the node   

#SBATCH --job-name=mgo_rel
#SBATCH --nodes=8
#SBATCH --tasks-per-node=64
#SBATCH --cpus-per-task=2
#SBATCH --time=24:00:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=e89-camc
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the job environment (this module needs to be loaded before any other modules)
module load PrgEnv-gnu
module load cray-python
module load cpe/21.09
module load cray-fftw

export LD_LIBRARY_PATH=/work/e89/e89/cwm31/prog/vasp/archer_dftd4/lib64:$LD_LIBRARY_PATH

# Load the VASP module, avoid any unintentional OpenMP threading by
# setting OMP_NUM_THREADS, and launch the code.
export OMP_NUM_THREADS=1

i=8
vaspinputs="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/au8/dft/inputs_au_gas"
poscars="/work/e89/e89/cwm31/03-DFT_Benchmarks/gasphase/au8/optstr"
element="au8"

for xc in pbe pbe-d2 pbe-ddsc pbe-d3 pbe-ts pbe-tshi pbe-d4 pbe-mbd pbe-mbdhi revpbe revpbe-d3 revpbe-ts revpbe-tshi revpbe-d4 vdw-df vdw-df2 optB86b-vdw rev-vdw-DF2 r2scan-d4 scan-rvv10 b3lyp-d2 b3lyp-d3 b3lyp-d4 pbe0 pbe0-d3 pbe0-d4 pbe0-tshi hse06-d4
do
for sys in AD #AD_SLAB #AD SLAB
do
rm -rf ${i}/${xc}/${sys}
mkdir -p ${i}/${xc}/${sys}

cp ${vaspinputs}/${xc}/${sys}/* ${i}/${xc}/${sys}
cp archer_vasp.sh ${i}/${xc}/${sys}
cp ${poscars}/POSCAR_${element}_${i} ${i}/${xc}/${sys}/POSCAR
cd ${i}/${xc}/${sys}
srun --distribution=block:block --hint=nomultithread /work/e89/e89/cwm31/prog/vasp/vasp_archer/vasp.6.3.0/bin/vasp_std > log

cd ../../../
done
done

