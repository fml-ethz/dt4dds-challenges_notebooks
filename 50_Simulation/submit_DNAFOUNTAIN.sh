#!/bin/bash
sbatch <<EOT
#!/bin/bash

#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=16G
#SBATCH --job-name=DNAF-"$1"
#SBATCH --output="$3"

python runner.py "$1" DNAFOUNTAIN "$2"
EOT
