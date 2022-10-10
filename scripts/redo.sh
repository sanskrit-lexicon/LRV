echo "Step1. Convert to Unix line-endings and store in lrv_1.txt."
python3 lrv_prep1.py ../interim/lrv_0.txt ../interim/lrv_1.txt
echo "Step2. Add metaline to lrv_1.txt and store in lrv_2.txt."
python3 lrv_prep2.py ../interim/lrv_1.txt ../interim/lrv_2.txt
echo "Step3. Add literary source and paragraph markups and store in lrv_3.txt."
python3 lrv_prep3.py ../interim/lrv_2.txt ../interim/lrv_3.txt
echo "Step4. Convert Devanagari to SLP1 and store in lrv_4.txt."
python3 lrv_prep4.py ../interim/lrv_3.txt ../interim/lrv_4.txt
echo "Step5. Keep only one headword in key1 out of alternate headwords."
python3 lrv_prep5.py ../interim/lrv_4.txt ../interim/lrv_5.txt

