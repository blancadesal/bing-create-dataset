#!/usr/bin/env bash

# get_images: Download media files from txt file containing
# list of urls using wget. Files that already exist
# in the target dir are not downloaded again.

display_usage() { 
	echo "Usage: ${0##*/} <source file> <target directory>" 
	} 

# If less than two arguments supplied, display usage 
	if [  $# -le 1 ]; then 
		display_usage
		exit 1
	fi

# Test if file exists
if [ ! -f "$1" ]; then
    echo "File "$1" does not exist"
    exit 1
fi

# Check if target directory path exists
BASE_DIR="$(dirname "$2")"
if [ ! -d "$BASE_DIR" ]; then
    echo ""$2" is not a valid directory"
    exit 1
fi

# Check if target directory exists already
if [ -d "$2" ]; then
  echo ""$2" exist already. Do you wish to proceed anyway?"
  read -n1 -p "[y/n] "  option
case $option in  
  y|Y) echo '' ;; 
  n|N) exit 0  ;; 
  *) exit 1 ;; 
esac
fi

# Create target directory if it doesn't exist already
mkdir -p $2

FILE_PATH="$1"
DEST_DIR="$2"

echo $FILE_PATH
echo $DEST_DIR

# Download images

echo 'Downloading images...'

wget -i $FILE_PATH --timeout=5 --tries=2 -P $DEST_DIR -N
