#!/bin/bash
file=$1
for w in $(tr 'A-Z ,."()?!;:' 'a-z\n' < $file); do echo ${#w} $w; done | sort -u | sort -n | cut -d " " -f2 > "${file}_sorted"
#for w in $(tr 'A-Z ,."()?!;:' 'a-z\n' < $file); do echo ${#w} $w; done | sort -u | sort -n > "${file}_sorted"
a="{"
lineno=2
for i in `seq 1 22`;
do
len=`tr ' ' '\n' <"${file}_sorted" | awk -v n=$i 'length($0)==n' | wc -l`
let lineend=$len+$lineno-1
a="${a}${i}:[$lineno,$lineend], "
let lineno=$lineno+$len
done  
a="$a}"
sed -i "1i $a" ./"${file}_sorted"
echo "Created sorted file "${file}_sorted""

if [ -d "wmat" ]; then
echo "Removing wmat directory"
rm -rf ./wmat
fi
mkdir wmat

python2 ./createwmat.py "${file}_sorted"


