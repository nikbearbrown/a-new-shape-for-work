#!/bin/bash
#SBATCH --job-name=job-shape-gsearch
#SBATCH --partition=short
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/gsearch-%j.log
module load python/3.13.5
cd /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work
python3 -I postings.py /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/out-gsearch gsearch-only
