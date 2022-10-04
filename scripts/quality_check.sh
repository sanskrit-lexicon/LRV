echo "Find out potential errors for examination."
echo "Step 1. Find duplicate page-sequence numbers, if any."
python3 duplicate_pc.py
echo "Step 2. Find duplicate lnums, if any."
python3 duplicate_lnum.py

