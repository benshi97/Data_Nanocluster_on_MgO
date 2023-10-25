#!/bin/bash

set -e

for i in Au Ag Cu
do
	for j in 4
	do
		for k in 1 2 3 4
		do
			for l in 1 2 # 3
			do
				if [ ${l} = 2 ]; then
					a=$(grep "Reference energy" ${i}${j}/LNOCC/${k}/3/mrcc.out | tail -n 1 | awk ' { print $4 } ')
				else
					a=$(grep "Reference energy" ${i}${j}/LNOCC/${k}/1/mrcc.out | tail -n 1 | awk ' { print $4 } ')
				fi
				b=$(grep "Reference energy" ${i}${j}/FNOCC/${k}/${l}/mrcc.out | tail -n 1 | awk ' { print $4 } ')
				echo "${i} ${j} ${k} ${l} ${a} ${b}"
			done
		done
	done
done
