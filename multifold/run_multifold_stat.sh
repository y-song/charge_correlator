#!/bin/bash

for i in {0..9}
do
	export PYTHONHASHSEED=0
	python3 multifold_test_stat.py ${i}
done
