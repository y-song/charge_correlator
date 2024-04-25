#!/bin/bash

for file in `cat geant_new.list`
	do
	#./bin/RunppTestAna -i '/gpfs01/star/pwg/elayavalli/ppRun12Embpicos/Cleanpp12Pico_pt25_35_g0.root' -intype pico -c JetTree -trig ppJP2 -o 'Results/geant/Geant'$file -N -1 -pj 10 2000 -mj 1 -pc 0.2 30 -lja antikt -ec 1 -R 0.4 -geantnum 1 -hadcorr 1 -towunc 0 -fakeeff 1 
	#./bin/RunppTestAna -i '/gpfs01/star/pwg/elayavalli/ppRun12Embpicos/'$file -intype pico -c JetTree -trig ppJP2 -o 'Results/geant/Geant'$file -N -1 -pj 10 2000 -mj 1 -pc 0.2 30 -lja antikt -ec 1 -R 0.4 -geantnum 1 -hadcorr 1 -towunc 0 -fakeeff 1 
	#./bin/RunppTestAna -i '/gpfs01/star/pwg/youqi/run12/embedding/P12id/picos/pp2012embed_2023/out/'$file -intype pico -c JetTree -trig all -o 'Results/geant/Geant'$file -N -1 -pj 5 2000 -mj 1 -pc 0.2 30 -lja antikt -ec 1 -R 0.4 -geantnum 1 -hadcorr 1 -towunc 0 -fakeeff 1 
	./bin/RunppTestAna -i '/gpfs01/star/pwg/youqi/run12/embedding/P12id/picos/pp2012embed_2023/out/'$file -intype pico -c JetTree -trig ppJP2 -o 'results/geant/Geant'$file -N -1 -pj 15 2000 -mj 1 -pc 0.2 30 -lja antikt -ec 1 -R 0.4 -geantnum 1 -hadcorr 1 -towunc 0 -fakeeff 1
done
