#!/bin/sh
#PBS -V
#PBS -N au20dft
#PBS -q normal
#PBS -A vasp
#PBS -l select=16:ncpus=16:mpiprocs=16:ompthreads=1
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR

#load modules
source ~/bin/initialize_conda.sh
conda activate intelpython
module purge
module load craype-mic-knl intel/18.0.3 impi/18.0.3
export TMI_CONFIG=/apps/compiler/intel/18.0.3/impi/2018.3.222/etc64/tmi.conf

mpirun vasp_std > log
