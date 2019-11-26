#!/bin/bash

function run_trab1 {
    SRC_FILE="exemplos/${1}.txt"
    RESULT_FILE="results/${1}.txt"
    echo "running for 'exemplos/${1}.txt'"
    setsid python trab1.py "${SRC_FILE}" > "${RESULT_FILE}"
} 

run_trab1  aabaaa
run_trab1  cccc
run_trab1  macaco
run_trab1  macaco_probs
