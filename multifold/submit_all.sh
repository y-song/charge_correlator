#!/bin/bash

for i in {1..40}
do
	sbatch submit.sh ${i}
done
