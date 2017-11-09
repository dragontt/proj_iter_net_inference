#!/bin/bash
#SBATCH -n 11
#SBATCH --mem-per-cpu=60G
#SBATCH -D ./scripts/
#SBATCH -J lasso
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=yiming.kang@wustl.edu

targetExpressionFile=${1}
regulatorExpressionFile=${2}
allowedMatrixFile=${3}
perturbationMatrixFile=${4}
microarrayFlag=${5}
nonGlobalShrinkageFlag=${6}
lassoAdjMtrFileName=${7}
combinedModelAdjMtrFileName=${8}
outputDirectory=${9}
combinedAdjLstFileName=${10}
regulatorGeneNamesFileName=${11}
targetGeneNamesFileName=${12}

echo "calling mpirun now, SLURM_NTASKS=${SLURM_NTASKS}"

mpirun -np ${SLURM_NTASKS} R --no-save -q --args ${targetExpressionFile} ${regulatorExpressionFile} ${allowedMatrixFile} ${perturbationMatrixFile} ${microarrayFlag} ${nonGlobalShrinkageFlag} ${lassoAdjMtrFileName} ${combinedModelAdjMtrFileName} ${outputDirectory} ${combinedAdjLstFileName} ${regulatorGeneNamesFileName} ${targetGeneNamesFileName} < run_lasso_parallel_init.r > ./log/lasso.out

