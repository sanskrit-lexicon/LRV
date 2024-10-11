10-11-2024
issue: https://github.com/sanskrit-lexicon/LRV/issues/25

# This directory
cd /c/xampp/htdocs/sanskrit-lexicon/LRV/issues/issue25

# Add {#X#} markup for the headword

Start with lrv.txt from csl-orig at commit
  e2a9d2d544d8d4532419caca292cf0f572e157b1

cd /c/xampp/htdocs/cologne/csl-orig
git show e2a9d2d544:v02/lrv/lrv.txt > /c/xampp/htdocs/sanskrit-lexicon/LRV/issues/issue25/temp_lrv_0.txt
cd /c/xampp/htdocs/sanskrit-lexicon/LRV/issues/issue25


------------------------------------
python make_lrv_1.py temp_lrv_0.txt temp_lrv_1.txt


53442 ^<L>  

47602 ¦
{{Lbody 5840

(+ 47602 5840) 53442 as expected

(* 3 53442) 160326  as expected

------------------------------------
local install using temp_lrv_1.txt

# regenerate local displays from temp_pwg_1
# This to check xml validity.

cp temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh lrv  ../../lrv
sh xmlchk_xampp.sh lrv
# ok  No problems noticed
cd /c/xampp/htdocs/sanskrit-lexicon/LRV/issues/issue25

-----------------------------------------
sync with github


sync csl-orig to github

cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "LRV: add missing {#..#} markup.
Ref: https://github.com/sanskrit-lexicon/lrv/issues/25"
git push

cd /c/xampp/htdocs/sanskrit-lexicon/PWG/pwgissues/issue77
-------------------------------
sync csl-orig at cologne
regenerate lrv displays at cologne
-------------------------------
sync this lrv repo to github

git add .
git commit -m "add {#X#} markup. #25"
git push
-------------------------------
THE END
