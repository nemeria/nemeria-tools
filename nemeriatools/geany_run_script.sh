#!/bin/sh

rm $0

python "views.py"

echo "

------------------
(program exited with code: $?)" 		


