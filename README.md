# Iterative Network Inference

Project description goes here...

### SYSTEM REQUIREMENTS
* Slurm workload manager (tested on v15.08.7)
* Open MPI (tested on v1.8.8)
* R (>= v3.2, tested on v3.2.1)
* Python (>= v2.7, tested on v2.7.10)

### CONFIGURATIONS

* Log in R/3.2.1 session to ensure Rmpi_0.6-5 & lars_0.9-8 are loaded. 
* Modify #SBATCH --mail-user=wustl.id@wustl.edu in ```run_lasso_parallel_init.sh``` to recieve notification of job progress.


### RUNNING NETWORK INFERENCE

	```
	export PATH=<projectDirectory>:$PATH
	sbatch run_lasso_parallel_init.sh <targetExpressionFile> <regulatorExpressionFile> \ 
	<allowedMatrixFile> <perturbationMatrixFile> <microarrayFlag> <nonGlobalShrinkageFlag> \ 
	<lassoAdjMtrFileName> <combinedModelAdjMtrFileName> <outputDirectory> \ 
	<combinedModelAdjLstFileName> <regulatorGeneNamesFile> <targetGeneNamesFile>
	```

### EVALUATE INFERENCE ACCURACY

	```
	```
