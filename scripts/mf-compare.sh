#!/bin/bash
## Following is an example of the expected command-line arguments.
#mf-compare.sh version_lower.txt version_upper.txt basename version_lower# version_upper#

cd "in"
paste ${1} ${2}						> ../tmp/mf-${3}-${4}_${5}.txt
cd "../tmp"
awk '{printf("%.4f\n",$2-$1)}' mf-${3}-${4}_${5}.txt	> mf-${3}-${4}_${5}-diff.txt 
paste mf-${3}-${4}_${5}.txt mf-${3}-${4}_${5}-diff.txt	> ../out/mf-${3}-${4}_${5}-final.txt
cd ".."
rm "tmp/*"
