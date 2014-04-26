#!/bin/bash

for i in $(seq 0 7);
do
    python simulation.py normal $i
done
