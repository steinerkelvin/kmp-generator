#!/bin/bash

function run_trab1 {
    setsid python trab1.py "exemplos/${1}.txt" > "results/${1}.txt"
} 

# run_trab1  aabaaa
run_trab1  cccc
# run_trab1  macaco
run_trab1  macaco_probs
