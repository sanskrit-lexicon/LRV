echo "Step 1. Revert lrv_4 to lrv_3."
python3 revert_4to3.py ../interim/lrv_4.txt ../interim/reversion/lrv_3.txt
echo "Print diff, if any"
diff ../interim/reversion/lrv_3.txt ../interim/lrv_3.txt
echo "Step 2. Revert lrv_3 to lrv_2."
python3 revert_3to2.py ../interim/lrv_3.txt ../interim/reversion/lrv_2.txt
echo "Print diff, if any"
diff ../interim/reversion/lrv_2.txt ../interim/lrv_2.txt
echo "Step 3. Revert lrv_2 to lrv_1."
python3 revert_2to1.py ../interim/lrv_2.txt ../interim/reversion/lrv_1.txt
echo "Print diff, if any"
diff ../interim/reversion/lrv_1.txt ../interim/lrv_1.txt

