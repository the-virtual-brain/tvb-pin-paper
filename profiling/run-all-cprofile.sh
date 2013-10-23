#!/bin/bash

for i in $(seq 0 7);
do
    python -m cProfile -o %i.cprof simulation.py cprof $i
done
