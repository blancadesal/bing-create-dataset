#!/usr/bin/env bash

# get_url_sample: Given a txt file containing urls,
# create random sample of size n and output as a new
# txt file. 

display_usage() { 
	echo "Usage: ${0##*/} [-n] SAMPLE SIZE <source file> <target file>" 
} 

# If less than four arguments supplied, display usage 
	if [  $# -le 3 ]; then 
		display_usage
		exit 1
	fi

# Test if source file exists
if [ ! -f "$3" ]; then
    echo "File "$3" does not exist"
    exit 1
fi

# Check if target file exists already
if [ -f "$4" ]; then
  echo ""$4" exist already. Do you wish to overwrite?"
  read -n1 -p "[y/n] "  option
case $option in  
  y|Y) printf "\n" ;; 
  n|N) exit 0  ;; 
  *) exit 1 ;; 
esac
fi

while getopts n: flag
do
    case "${flag}" in
        n) sample_size=${OPTARG};;
    esac
done

SOURCE_FILE="$3"
TARGET_FILE="$4"

shuf -n $sample_size $SOURCE_FILE > $TARGET_FILE