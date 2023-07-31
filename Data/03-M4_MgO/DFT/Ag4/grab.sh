#!/bin/bash

set -e

for i in 1 2 3 4
do
	cp ${i}/pbe/AD_SLAB/POSCAR POSCAR_${i}
done
