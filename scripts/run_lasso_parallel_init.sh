#!/bin/bash
#SBATCH -n 11
#SBATCH --mem-per-cpu=20G
#SBATCH -D scripts/
#SBATCH -J lasso
#SBATCH -o ../log/lasso.out
#SBATCH -e ../log/lasso.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=yiming.kang@wustl.edu

targetExpressionFile=${1}
regulatorExpressionFile=${2}
allowedMatrixFile=${3}
perturbationMatrixFile=${4}
lassoAdjMtrFileName=${5}
outputDirectory=${6}

module load R/3.2.1
module load openmpi

echo "calling mpirun now, SLURM_NTASKS=${SLURM_NTASKS}"

mpirun -np ${SLURM_NTASKS} R --no-save -q --args ${targetExpressionFile} ${regulatorExpressionFile} ${allowedMatrixFile} ${perturbationMatrixFile} ${lassoAdjMtrFileName} ${outputDirectory} < run_lasso_parallel_init.r > ../log/r.out

