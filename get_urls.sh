#!/usr/bin/env bash

# get_urls: Extract media (image, gif, video) urls
# from sites supported by dl-gallery
# https://github.com/mikf/gallery-dl

# TODO: specify file type (i.e JPG, MP4, etc) as an optional parameter.
# Right now the script is hardcoded for JPG only. 

display_usage() { 
	echo "Usage: ${0##*/} <source directory> <target file>" 
	} 

# If less than two arguments supplied, display usage 
	if [  $# -le 1 ]; then 
		display_usage
		exit 1
	fi

# Check if source directory exists
if [ ! -d "$1" ]; then
    echo ""$2" is not a valid directory"
    exit 1
fi

# Check if target directory exists
DEST_DIR="$(dirname "$2")"
if [ ! -d "$DEST_DIR" ]; then
    echo ""$2" is not a valid directory"
    exit 1
fi

# Check if target file exists already
if [ -f "$2" ]; then
  echo ""$2" exist already. Do you wish to overwrite?"
  read -n1 -p "[y/n] "  option
case $option in  
  y|Y) printf "\n" ;; 
  n|N) exit 0  ;; 
  *) exit 1 ;; 
esac
fi

SOURCE_DIR=$1
DEST_FILE=$2

tmpfile=$(mktemp)

# Download urls
echo 'Downloading urls...'

for f in $SOURCE_DIR/*.txt
do

gallery-dl -g --range 1-10 -i $f >> $tmpfile

done

# Filter for desired file type (JPG only at the moment - TODO)
grep ".*\.jpg$" $tmpfile > $DEST_FILE 
rm $tmpfile

url_count=$(wc -l < $DEST_FILE)
echo "$url_count image urls saved to file"