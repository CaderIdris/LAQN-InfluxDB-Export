#!/bin/bash

venv=venv/bin/python3

echo "Start Year? (YYYY-MM-DD): "
read startdate
echo "End Year? (YYYY-MM-DD): "
read enddate

$venv main.py -s $startdate -e $enddate
