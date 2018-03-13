#!/bin/bash
## Following is an example by use of the requisite command-line arguments.
#./mf-extraction.sh listing_file.dat output_file.dat#

cat -v $1 | grep "IN - OUT" | sed -- 's/^\s\s*IN - OUT =\s*\([-0-9.]*\).*$/\1/' > $2
