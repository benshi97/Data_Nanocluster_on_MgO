#!/bin/sh
#PBS -V
#PBS -N au20dft
#PBS -q debug
#PBS -A vasp
#PBS -l select=2:ncpus=68:mpiprocs=68:ompthreads=1
#PBS -l walltime=10:00:00

cd $PBS_O_WORKDIR

#load modules
source ~/bin/initialize_conda.sh
conda activate intelpython
module purge
module load craype-mic-knl intel/18.0.3 impi/18.0.3
export TMI_CONFIG=/apps/compiler/intel/18.0.3/impi/2018.3.222/etc64/tmi.conf

mpirun -np 32 vasp_std > log
