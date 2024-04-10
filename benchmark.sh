#!/bin/bash
# usage
# bash ./benchmark.sh arg1 arg2
# arg1 target parent directory with the test cases 
# arg2 name of the output file to write the benchmark times to. 

echo "" > $2 

# Check if the '$1' directory exists
if [ -d "$1" ]; then
    for file in $1/*; do
		#echo "time python3 algorithm.py $file > $folder_name/$(basename "$file")_benchmark.sol"
		#time -p python3 algorithm.py $file > $folder_name/$(basename "$file")_benchmark.sol
		echo "time python3 algorithm.py $file" >> $2
		{ time python3 algorithm.py $file; } 2>> $2
		echo "------------------------------" >>$2
    done
else
    echo "The '$1' directory does not exist in the current working directory."
fi