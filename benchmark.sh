#!/bin/bash

for a in 0.15 0.25 0.3
do
	for b in 1.2 2.0 2.7 3.6
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
