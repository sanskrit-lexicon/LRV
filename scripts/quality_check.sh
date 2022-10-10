echo "Find out potential errors for examination."
echo "STEP 1. Find duplicate page-sequence numbers, if any."
echo "Ideal - no diff."
echo ""
python3 qc_duplicate_pc.py
echo "Step 2. Find duplicate lnums, if any."
echo "Ideal - no diff."
echo ""
python3 qc_duplicate_lnum.py
echo "Step 3. Find unique headwords and store in logs/issue11/unique_headwords.txt for manual examination."
python3 qc_unique_headwords.py
echo ""
echo "Step 4. Find headwords having differences between k1 and k2."
echo "Ideal - no diff."
python3 qc_hw_k2_diff.py

