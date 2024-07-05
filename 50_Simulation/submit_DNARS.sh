#!/bin/bash
sbatch <<EOT
#!/bin/bash

#SBATCH -n 1
#SBATCH --cpus-per-task=18
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=500M
#SBATCH --job-name=DNARS-"$1"
#SBATCH --output="$3"

export OMP_NUM_THREADS=18
export OMP_DYNAMIC=false
python runner.py "$1" DNARS "$2"
EOT
