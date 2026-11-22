#!/bin/bash
#SBATCH --job-name=job-shape-postings
#SBATCH --partition=short
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/postings-%j.log
module load python/3.13.5
cd /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work
python3 -I postings.py /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/out
