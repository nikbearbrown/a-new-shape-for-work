#!/bin/bash
# Fetch the two public inputs into source/ (each into its own folder), with sizes and sha256 printed for the README.
# Run from the repo root:  bash scripts/fetch_sources.sh
# On the Explorer cluster O*NET 31.0 is already at /projects/aiskunks/onet/31.0/db_31_0_text: copy instead of downloading.
set -euo pipefail
mkdir -p source/onet-31.0 source/anthropic-economic-index/labor-market-impacts

# 1. O*NET 31.0 text database (CC BY 4.0, USDOL/ETA), 13,183,034 bytes,
#    sha256 6883548adf5fde64cf6f801b35d15519c9225f2732c3cab0e281c652d16b23a9
if [ ! -f "source/onet-31.0/Task Ratings.txt" ]; then
  if ssh -o BatchMode=yes -o ConnectTimeout=10 explorer true 2>/dev/null; then
    for f in "Task Statements.txt" "Task Ratings.txt" "Tasks to DWAs.txt" "GWAs to IWAs to DWAs.txt" "GWAs to IWAs.txt" \
             "Work Activities.txt" "Occupation Data.txt" "Content Model Reference.txt" "Job Zones.txt" "Emerging Tasks.txt" \
             "Job Titles.txt" "Sample of Reported Titles.txt" "Read Me.txt"; do
      scp -q "explorer:/projects/aiskunks/onet/31.0/db_31_0_text/$f" source/onet-31.0/
    done
  else
    curl -sSL -o /tmp/db_31_0_text.zip https://www.onetcenter.org/dl_files/database/db_31_0_text.zip
    shasum -a 256 /tmp/db_31_0_text.zip
    unzip -q -j /tmp/db_31_0_text.zip 'db_31_0_text/*' -d source/onet-31.0
  fi
fi

# 2. Anthropic Economic Index task coverage (data CC-BY), pinned to dataset commit 4e5f69f, 1,889,822 bytes,
#    sha256 85bee872db1d55d3e9a7f4e89da5ae4a5d59aa8ec875d728fbf4b7d820984616
AEI=source/anthropic-economic-index/labor-market-impacts/task_penetration.csv
if [ ! -f "$AEI" ]; then
  curl -sSL -o "$AEI" \
    "https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6/labor_market_impacts/task_penetration.csv"
fi
shasum -a 256 "$AEI"
ls -l source/onet-31.0 | head -20
