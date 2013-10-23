#!/bin/bash

for i in $(seq 0 7);
do
	valgrind --tool=massif --massif-out-file=massif-$i --time-unit=ms python simulation.py massif $i
	ms_print massif-$i | python massif_snapshots.py > massif-$i-snapshots.txt
done

