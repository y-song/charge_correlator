#!/bin/bash

#SBATCH --time=2:0:00
#SBATCH --gpus=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=30G

if [ ! -d 'seed'$1 ]
then
	mkdir 'seed'$1
	cp pythia8_newemb_7d_unfold_7d_newreweight_largebatch_092523.py 'seed'$1
	cd 'seed'$1
	#conda activate my_env
	#srun test.py
	srun python pythia8_newemb_7d_unfold_7d_newreweight_largebatch_092523.py $1
	echo "Job for seed $1 is finished."
else
	echo "Skipping job for seed $1"
fi
