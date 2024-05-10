#!/bin/bash

# Manpage: https://slurm.schedmd.com/sbatch.html

##################################
######### Configuration ##########
##################################
# Configure the job name
#SBATCH --job-name NETS_Script_MultiGPU

##################################
####### Resources Request ########
##################################

# Use GPU partition (gpu1 and gpu2) or other partition (e.g.: short)
# Find more usable partitions with 'sinfo -a'
#SBATCH --partition=gpu1

# Configure the number of nodes (in partition above)
# NEVER use --ntasks-per-node > 1 if you are not using MPI
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
# Configure the number of GPUs
#SBATCH --gpus-per-node=4
#SBATCH --exclusive
#SBATCH --mem=0
# Set time limit 3 days
#SBATCH --time=3-00:00:00

echo `date`
# load conda environment (leave <env_name> empty if you want to load base env)
. ./env.sh <env_name>

start=`date +%s`

# Run the training script
python queuerun.py

end=`date +%s`

runtime=$((end-start))
echo "Runtime: $runtime"
