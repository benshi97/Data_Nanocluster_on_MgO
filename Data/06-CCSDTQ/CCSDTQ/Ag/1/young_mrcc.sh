#!/bin/bash -l
#$ -N EMBD
#$ -l h_rt=24:00:00
#$ -P Gold
#$ -A UKCP_CAM_C
#$ -l mem=185G
#$ -ac allow=Z
#$ -pe smp 16
#$ -cwd


WORKDIR=${PWD}

export PATH="/home/mmm0606/Programs/mrcc_2022_mpi:$PATH"
export OMP_NUM_THREADS=36
export MKL_NUM_THREADS=36
export OMP_PLACES=cores
export OMP_PROC_BIND=spread,close


# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
WORKDIR=${PWD}

# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
cd /dev/shm
df -h > $WORKDIR/shm.out
mkdir -p mmm0606/
rm -rf mmm0606
mkdir -p mmm0606/
cd mmm0606

cp $WORKDIR/MINP .


/home/mmm0606/Programs/mrcc_2022_mpi/dmrcc MINP | tee $WORKDIR/mrcc.out $WORKDIR/mrcc.out.$JOB_ID

cd ../
rm -rf mmm0606

