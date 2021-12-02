#!/bin/bash
fname=$1
let prev=0
let gt=-1
let lt=0
while IFS= read -r line
do
	if ((line > prev)) 
	then
		echo "$line > $prev"
		let gt++
	elif ((line < prev))
	then
		echo "$line < $prev"
		let lt++
	else
		echo "no change"
	fi
	let prev=line
done < $fname

echo "GT: $gt"
echo "LT: $lt"