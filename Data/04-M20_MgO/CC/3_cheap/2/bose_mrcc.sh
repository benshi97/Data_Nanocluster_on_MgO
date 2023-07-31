#!/bin/bash

# pe request
#$ -pe mpi_20 20
#mpi_number of cores to use in one node total#of cores to use
# our Job name 
#$ -N au20

#$ -S /bin/bash

#$ -q 1st.q
#$ -V

#$ -cwd

# needs in 
#   $NSLOTS          
#       the number of tasks to be used
#   $TMPDIR/machines 
#       a valid machiche file to be passed to mpirun 
#   enables $TMPDIR/rsh to catch rsh calls if available

echo "Got $NSLOTS slots."
cat $TMPDIR/machines

#######################################################
### openmpi 1.6.4 (w/ Intel compiler)
#######################################################

source /home0/compiler/intel/oneapi/setvars.sh
export LD_PRELOAD="/home/hmran/prog/gcclib/glibc-2.15/lib/libc.so.6"

export PATH="/home/cwmyung/Ben_Programs/mrcc_binary/mrcc_2022:$PATH"
export OMP_NUM_THREADS=20
export MKL_NUM_THREADS=20
export OMP_PLACES=cores
export OMP_PROC_BIND=spread,close

cp MINP_PBE MINP
/home/cwmyung/Ben_Programs/mrcc_binary/mrcc_2022/dmrcc MINP | tee mrcc_PBE.out mrcc_PBE.out.$JOB_ID
cp MINP_CC MINP
/home/cwmyung/Ben_Programs/mrcc_binary/mrcc_2022/dmrcc MINP | tee mrcc.out mrcc.out.$JOB_ID
