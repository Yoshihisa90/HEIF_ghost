#!/bin/bash
#SBATCH -J encode_second

#SBATCH --mem=2G                                            # RAM requirements
#SBATCH --ntasks=1                                          # Tasks requirements
#SBATCH --cpus-per-task=1                                   # CPUs (i.e. cores) per task
#SBATCH --nodes=1                                           # Number of nodes (i.e. how many servers)

#SBATCH --mail-user=yoshihisa.furushita@unifi.it            # Email address of job owner
#SBATCH --output=logs/encode_single_%j_%N_%x_%A_%a.log              # Log file (regular output)
#SBATCH --error=logs/encode_single_%j_%N_%x_%A_%a.log               # Log file (error output)

#SBATCH --array=0-269

LIBHEIF_PATH=/usr/bin/heif-enc
CONVERT_PATH=/usr/bin/heif-convert
INPUT_DIR=/Prove/Yoshihisa/HEIF_ghost/HEIF_IMAGES_LIBHEIF/HEIF_images_triple
OUTPUT_DIR=/Prove/Yoshihisa/HEIF_ghost/PKL/pkl_triple

source "/data/lesc/staff/yoshihisa/anaconda3/etc/profile.d/conda.sh"

./2-creating_data.py -l "$LIBHEIF_PATH" -c "$CONVERT_PATH" -i "$INPUT_DIR" -o "$OUTPUT_DIR" run-triple ${SLURM_ARRAY_TASK_ID}
