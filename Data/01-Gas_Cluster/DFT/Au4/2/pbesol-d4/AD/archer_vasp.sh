#!/bin/bash

# Request 16 nodes (1024 MPI tasks at 64 tasks per node) for 3 hours
# Note setting --cpus-per-task=2 to distribute the MPI tasks evenly
# across the NUMA regions on the node   

#SBATCH --job-name=mgo_rel
#SBATCH --nodes=4
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
srun --distribution=block:block --hint=nomultithread /work/e89/e89/cwm31/prog/vasp/vasp_archer/vasp.6.3.0/bin/vasp_std > log
