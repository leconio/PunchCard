#!/bin/sh

cd /Users/spawn/PycharmProjects/PunchCard/

echo `date` >> run.log &&

/usr/local/bin/python3 /Users/spawn/PycharmProjects/PunchCard/punch.py

echo 'finish' >> run.log