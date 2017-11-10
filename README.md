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
Run LASSO regression to infer TF-gene network, using the TF activity matrix inferred from TFA algorithm and gene expression matrix. This module is designed to be combined with TFA module to iteratively refine the inferred network.

	```
	export PATH=<projectDirectory>:$PATH
	sbatch run_lasso_parallel_init.sh <targetExpressionFile> <regulatorActivityFile> <allowedMatrixFile> \
	<perturbationMatrixFile> <lassoAdjMtrFileName> <outputDirectory>
	```

### EVALUATE INFERENCE ACCURACY
Evaluate the performance of iteractive network inference, against two benchmarks (1) network built from ChIP-chip/seq experiments (measure TF binding strength) (2) network built from DNA-binding motif (computaitonal model) of TFs (TF binding potentials).


	```
    sbatch scripts/run_evaluate_network.sh <networkFile> 32 20
	```

### DESCRIPTIONS OF DATA FILES
FILE | DESCRITPION
--- | ---
targetExpressionFile | A matrix of the expression values of all genes measured. Rows represent genes, columns represent samples/conditions, i.e. the matrix dimension is number of genes x number of samples.
regulatorActivityFile | A matrix of the activities of all TF inferred. Rows represent TFs, columns represent samples/conditions, i.e. the matrix dimension is number of TFs x number of samples.
allowedMatrixFile | A space separated binary adjacency matrix of size # of TFs (rows) x # of target genes (columns). For each possible interaction between TF i (Ri) and target gene j (Tj), entry Mij is set to 1 if Ri is allowed to regulate Tj and 0 if Ri is not allowed to regulate Tj. Users should disallow auto-regulation by setting Mij = 0 when Ri==Tj.
perturbationMatrixFile | A space separated binary matrix of size # of target genes (rows) x # of expression conditions (columns). Each entry Mij is set to 0 if target gene i (Ti) is not experimentally perturbed (e.g. overexpressed, knocked down, or knocked out) in condition j (Cj). Thus, Mij = 1 if Ti is perturbed in Cj and Mij = 0 otherwise.



