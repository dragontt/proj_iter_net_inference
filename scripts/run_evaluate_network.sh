#!/bin/bash
#SBATCH --mem=2G
#SBATCH -D scripts/
#SBATCH -J evaluation
#SBATCH -o ../log/evaluation.out
#SBATCH -e ../log/evaluation.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=yiming.kang@wustl.edu

NETWORK=$1
MAXRANK=$2
NUMBINS=$3
DIR_ANALYSIS=$4

if [ -z $NUMBINS ]; then NUMBINS=20; fi
MINRANK=$(bc <<< "scale=3; $MAXRANK/$NUMBINS")
if [ -z $DIR_ANALYSIS ]; then DIR_ANALYSIS=../output; fi

module load R/3.2.1

## benchmarking files
REGS=../resources/rids_full.txt
GENES=../resources/gids_full.txt
CHIP_NET=../benchmarks/chip_net.txt
PWM_NET=../benchmarks/motif_net.txt

## over adjacency matrix to adjacency list
ADJLST=../tmp/${NETWORK##*/}.txt
NAME_ANALYSIS=${NETWORK##*/}
NAME_ANALYSIS=${NAME_ANALYSIS%.adjmtr}
sed -i 's/ /\t/g' ${NETWORK}
echo -e "REGULATOR\tTARGET\tCONFIDENCE" > ${ADJLST}
adjmtr2interactions.rb -a ${NETWORK} -r ${REGS} -c ${GENES} >> ${ADJLST}

## evaluate network in NetProphet style
Rscript evaluate_network.r ${ADJLST} ${CHIP_NET} ${PWM_NET} ${DIR_ANALYSIS}/evaluation.${NUMBINS}bins.top${MINRANK}to${MAXRANK}k.${NAME_ANALYSIS}.txt ${MAXRANK} ${NUMBINS}

rm ${ADJLST}
