echo "Step1."
python3 lrv_prep1.py ../interim/lrv_0.txt ../interim/lrv_1.txt
echo "Step2."
python3 lrv_prep2.py ../interim/lrv_1.txt ../interim/lrv_2.txt
echo "Step3."
python3 lrv_prep3.py ../interim/lrv_2.txt ../interim/lrv_3.txt
echo "Step4."
python3 lrv_prep4.py ../interim/lrv_3.txt ../interim/lrv_4.txt
