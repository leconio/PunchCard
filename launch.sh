#!/bin/sh

cd /Users/spawn/PycharmProjects/PunchCard/

echo `date` >> run.log &&

python3 punch.py

echo 'finish' >> run.log