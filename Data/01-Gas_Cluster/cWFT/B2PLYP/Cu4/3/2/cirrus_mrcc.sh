#!/bin/bash

# Slurm job options (name, compute nodes, job time)
#SBATCH --job-name=bench
#SBATCH --time=96:00:0
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=36

# Replace [budget code] below with your budget code (e.g. t01)
#SBATCH --account=ec214
# We use the "standard" partition as we are running on CPU nodes
#SBATCH --partition=standard
# We use the "standard" QoS as our runtime is less than 4 days
#SBATCH --qos=standard

# Load any required modules
module load intel-tools-19/19.0.0.117

# Change to the submission directory
cd $SLURM_SUBMIT_DIR

# Set the number of threads to the CPUs per task
export PATH="/work/ec214/ec214/bxs_cirrus/Programs/mrcc_2022:$PATH"
export OMP_NUM_THREADS=36
export MKL_NUM_THREADS=36
export OMP_PLACES=cores
export OMP_PROC_BIND=spread,close

# Launch the parallel job
#   Using 36 threads per node
#   srun picks up the distribution from the sbatch options

WORKDIR=${PWD}
TMPDIR="/scratch/space1/ec214/bxs21/$SLURM_JOB_ID"
mkdir -p $TMPDIR
cd $TMPDIR
cp $WORKDIR/* $TMPDIR

/work/ec214/ec214/bxs_cirrus/Programs/mrcc_2022/dmrcc | tee $WORKDIR/mrcc.out $WORKDIR/mrcc.out.$SLURM_JOB_ID
