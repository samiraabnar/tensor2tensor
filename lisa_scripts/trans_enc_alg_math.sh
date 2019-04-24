#!/bin/bash

#SBATCH --job-name=attention_arithmatic
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=5:00:00
#SBATCH --partition=gpu_shared
#SBATCH --gres=gpu:1

module load eb
module load Python/3.6.3-foss-2017b
module load CUDA/10.0.130
module load cuDNN/7.3.1-CUDA-10.0.130
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:/hpc/eb/Debian/cuDNN/7.3.1-CUDA-10.0.130/lib64:$LD_LIBRARY_PATH

cd /home/samigpu/Codes/tensor2tensor

conda activate myt2t
HEAD_DIR=/home/samigpu/Codes/tensor2tensor/

DATA_DIR=$HEAD_DIR/data/algorithmic/
LOGS_DIR=$HEAD_DIR/logs
MODEL=transformer_encoder
HPARAM=transformer_tiny
PROBLEM=algorithmic_math_two_variables

t2t-trainer   --data_dir=$DATA_DIR   \
--problem=$PROBLEM  \
--model=$MODEL \
--hparams_set=$HPARAM \
--output_dir=$LOGS_DIR/$PROBLEM/$MODEL'_'$HPARAM