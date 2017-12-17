#!/bin/bash

while true
do
	echo "$(python acovrp.py instances/A/A-n32-k5.vrp 784)" >> "benchmark.txt"
done