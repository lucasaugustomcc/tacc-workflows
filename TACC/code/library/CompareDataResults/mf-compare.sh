#!/bin/bash
## Following is an example of the expected command-line arguments.
#mf-compare.sh version_lower.txt version_upper.txt basename version_lower# version_upper#

paste ${1} ${2}						> mf-bw.txt
awk '{printf("%.4f\n",$2-$1)}' mf-bw.txt	> mf-bw-diff.txt 
paste mf-bw.txt mf-bw-diff.txt	> ${3}
unlink mf-bw.txt
unlink mf-bw-diff.txt
