#!/bin/bash
## Following is an example by use of the requisite command-line arguments.
#./mf-extraction.sh listing_file.dat basename modflow_version#

mkdir $WORK/work
cat -v $1 $2 $3 | grep "IN - OUT" | sed -- 's/^\s\s*IN - OUT =\s*\([-0-9.]*\).*$/\1/' > $WORK/work/in/mf-$2-$3.txt
