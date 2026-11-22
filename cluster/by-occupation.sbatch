#!/bin/bash
#SBATCH --job-name=new-shape-by-occupation
#SBATCH --partition=short
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=03:00:00
#SBATCH --output=/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/by-occupation-%j.log
# Usage: sbatch by-occupation.sbatch            (all postings)
#        sbatch by-occupation.sbatch --limit 50000   (smoke test)
module load python/3.13.5
cd /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work
python3 -I postings_by_occupation.py /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/title-map.tsv /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/out-by-occupation "$@"
