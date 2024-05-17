This README explains my workflow for STAR analysis psn0829. To run the code in your directory, remember to change all the occurrences of `/gpfs01/star/pwg/youqi` to your own directories. Please contact me via youqi.song@yale.edu for any questions or comments.

Files are imported from `/gpfs01/star/pwg/youqi/run12/final` on RACF.

# Create ROOT trees as input to MultiFold

### Data trees

TStarJetPicos: The data used in this analysis are TStarJetPicos, which I have copied to the `raw_data/` folder under my work directory. For more information on TStarJetPicos, including how to produce them, see https://www.star.bnl.gov/cgi-bin/protected/cvsweb.cgi/offline/paper/psn0647/. psn0647, psn0718 and psn0743 also run on TStarJetPicos.

Compiling the code: For some reason that I don't understand, even though I have included `make` in `container.sh` in line 6, I need to compile the code before doing job submissions:
0. Pull the singularity container via `singularity pull --name star_test.simg docker://rkunnawa/star_user:latest`. Rename `star_test.simg` to `star_star.simg`.
1. Enter the singularity container by `source runimage.sh`
2. Once inside the container, do `source setup.sh`
3. Compile: do `mkdir bin`, and then `make`
4. Quit the singularity container by doing Ctrl+d

Job submission: The directory I use for job submission is `submit/` under my work directory. Inside the directory there is `submit.py` and `submit.xml`:
`submit/submit.py` - I have a for loop that loops over all the files in the file list `raw_data.list` (short list for code QA: `raw_data_short.list`). One job will be submitted for each iteration of the loop. In each loop, I defined a string "submit_args" which contains arguments "out", "log", "data_file", and they will be passed to `submit/submit.xml`
`submit/submit.xml` - Line 5 allows us to enter the singularity container. This is the equivalent of `source runimage.sh` when I run the code interactively. The options -B are directories that we want to be visible inside the container. It calls `container.sh` with singularity and reads the arguments "out", "log", and "data_file". "data_file" will then be passed to `container.sh`. I included the all TStarJetPicos data in the SandBox, which is not the best way of doing it but makes my life easier.
5. Create a folder for output via `mkdir results/data` (this is specified in the `-o` option in `container.sh`). 
6. Submit jobs via `python submit/submit.py`
7. Enter the container again to hadd the output files `out_sum*.root` to `data.root`

For code QA person: Ignore step 7. Your output file after step 6 would show up as `results/data/out_sum0.root`. It should be identical to `/gpfs01/star/pwg/youqi/run12/final/results/data/data.root`.

### Embedding trees

TStarJetPicos: Embedding trees are also in the form of TStarJetPicos, and are located at `/gpfs01/star/pwg/youqi/run12/embedding/P12id/picos/pp2012embed_2023/out`. The scripts for generating these trees from mini MCs and MuDSTs are in `/gpfs01/star/pwg/youqi/TStarJetPicoMaker` and instructions for running these scripts are in `MiniMcsToTStarJetPicos.txt`. The directory is copied from `/star/u/imooney/TStarJetPicoMaker`, except that the lists in `list_ppLargeStats/` have been modified with `remove_badruns.ipynb`. For code QA person, you do not have to remake these TStarJetPicos. The list of TStarJetPico root files `geant_new.list` (short list for code QA: `geant_short.list`) will be read in by shell scripts in steps 3 and 4 below.

0. Create output directories: `results/pythia`, `results/geant` and `results/matched`.

Turn off cut on vz (This is because we don't want to reduce efficiency due to high |vz|. We will remove events with bad vz later with the script that does matching between particle-level and detector-level):
1. In `src/ppTestParameters.hh`, change `double VzCut = 30` to `double VzCut = 999`.

Run code:
2. Enter the container and compile by following steps 1-3 of data trees procedure. Don't exit the container afterwards.
3. Create particle-level trees by running `./run_pythia_analysis.sh`. Hadd the output files in `results/pythia/` to a single file `pythia.root`
4. Create detector-level trees by running `./run_genat_analysis_new.sh`. Hadd the output files in `results/geant/` to a signle file `geant.root`

Match detector-level jets to particle-level and remove bad events:
5. Run `root -l 'MatchGeantToPythia.cxx+("pythia.root", "geant.root", "matched.root")'`
 
For code QA person: Your output file would show up as `results/matched/matched.root`. This file should be identical to `/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root`.

#  Run MultiFold

conda environment: MultiFold is done on Yale's computing cluster Grace. I created a conda environment called "my_env_2" that includes the dependencies needed. Relevant code is copied to `/gpfs01/star/pwg/youqi/run12/final/multifold/`. Within it, there is `environment.yml` which contains information about this conda environment. (Perhaps delete the following sentence: A lot of these packages are installed automatically. The packages that I manually installed and are needed are: matplotlib, numpy, pandas, python, and uproot).

Other packages: Tensorflow and energyflow are installed with pip. See instructions from https://www.tensorflow.org/install/pip and https://energyflow.network/installation/#install-via-pip.

Now, since code QA person needs to run my code on RACF, I tried the following to recreate the conda environment I have on Grace. However, as for the packages installed via `pip` by default, they will be the newest versions, while the packages I have on Grace are not.

Install software:
0.1 Install miniconda on RACF, following the instructions for Linux on https://docs.anaconda.com/free/miniconda/. Check that the installation is successful via `conda list`.
0.2 Recreate my conda environment via `conda env create -n my_env_2 -f environment.yml`. Enter the conda environment via `conda activate my_env_2`.
0.3 Install tensorflow on RACF: `python -m pip install tensorflow`. See instructions from https://www.tensorflow.org/install/pip
0.4 Install energyflow on RACF `pip install energyflow`. See instructions from https://energyflow.network/installation/#install-via-pip
 
MultiFold code: `multifold.py` is what I ran for my analysis. `multifold_test.py` has adjusted parameters for faster running for code QA, and accomodates some requirements by the newer version of tensorflow. 

Run MultiFold:
1. Do `cd /gpfs01/star/pwg/youqi/run12/final/multifold`. Edit Line 202 of `multifold_test.py` to put in a directory that you would like to save the output to. If you have confirmed that your ROOT trees from the previous step "Create ROOT trees as input to MultiFold" are identical to what I have, then you don't need to change the file paths for `data.root` and `matched.root`. Otherwise, don't forget to change the directories in Lines 127 and 134. 
2. Do `python3 multifold_test.py 0`
3. After MultiFold is done, you should be able to find `jet_noweight.csv`, `it1_seed0.csv`, `it2_seed0.csv`, `it3_seed0.csv`, `it4_seed0.csv`, and `it5_seed0.csv` in the directory that you specified in Line 202. Please let me know if these files are identical to the ones at `/gpfs01/star/pwg/youqi/run12/final/results/multifold_output`.

# Make plots with output from MultiFold

0. Enter the conda environment via `conda activate my_env_2`.
1. Go to `/gpfs01/star/pwg/youqi/run12/final/plot`. In all of the python scripts, change the directories `/gpfs01/star/pwg/youqi/run12/final` to where your files are located (but don't change `/gpfs01/star/pwg/youqi/run12/mc`). 
2. Do `python3 fig1.py`, `python3 fig2.py` and `python3 fig3.py`.
3. Check if the output plots are identical to the ones at `/gpfs01/star/pwg/youqi/run12/final/results/plot`.

# To do for Youqi

Prepare for instructions for recreating the statistical and systematic uncertainties.