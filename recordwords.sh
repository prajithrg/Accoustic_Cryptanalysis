#!/bin/bash

echo $samples

while read inputline; 
do
word="$inputline"
if [ -z "${word}" ];
then
exit
fi

let samples=${#word}*48000
echo "Samples:"$samples
echo "Type the word:"$word
python2 audio_to_file.py  -I hw:0,0 -N $samples $1$word
echo -e "\nWord saved" 
echo -e "\nEnter new word:"
done

