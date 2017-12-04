#!/bin/bash

for a in 0.05 0.1 0.2
do
	for b in 0.8 1.6 2.3 3.1
	do
		for q in 0.3 0.5 0.7 0.9
		do
			for m in 5 15 25
			do
				echo "$a $b $q $m $(python acovrp.py instances/A/A-n32-k5.vrp 784 -a $a -b $b -q $q -m $m)" >> "benchmark.txt"
			done
		done
	done
done
