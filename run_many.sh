#!/bin/bash

if [ $# -eq 2 ]; then
start=$1
end=$2
else
start=$((RANDOM % 2295))
end=$((start + RANDOM % (2295 - start)))
fi

for n in $(seq $start $end); do
current_hour=$(date +"%H")
#if [ "$current_hour" -ge 1 ] && [ "$current_hour" -lt 10 ]; then
#echo "Current time is between 1 AM and 10 AM. Waiting to proceed."
#sleep 3600
#n=$((n-1))
#continue
#else
./run_eval.sh $n
#fi
done

