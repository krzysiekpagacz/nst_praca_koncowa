#! /bin/bash
RAW_DUMPS_FOLDR=../resources/netflow_raw
CSV_DUMPS_FOLDR=../resources/netflow_csv
FORMAT=".csv"

for f in $RAW_DUMPS_FOLDR/*
do
	file=$(basename $f)
	echo procesing file: $file
	nfdump -r $RAW_DUMPS_FOLDR/$file -o csv > $CSV_DUMPS_FOLDR/$file$FORMAT
	chmod 777 $CSV_DUMPS_FOLDR/*.csv
done

