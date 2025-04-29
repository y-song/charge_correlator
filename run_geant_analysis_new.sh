#!/bin/bash

for file in `cat /gpfs01/star/pwg/youqi/run12/final_0628/20235003_filename.list`
	do
	./bin/RunppTestAna -i '/gpfs01/star/pwg/youqi/run12/embedding/P12id/picos/20235003/out/'$file -intype pico -c JetTree -trig ppJP2 -o '/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/geant/Geant'$file -N -1 -pj 15 2000 -pc 0.2 30 -lja antikt -ec 1 -R 0.4 -geantnum 1 -hadcorr 1 -towunc 0 -fakeeff 1
done
