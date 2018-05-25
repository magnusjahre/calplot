#!/bin/bash

echo
echo "Running plot tests"
echo
python calplotTest/plotTest.py

echo
echo "Running merge tests"
echo
python calplotTest/mergeTest.py
