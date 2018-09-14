#!/bin/sh

cd /Users/spawn/PycharmProjects/PunchCard/

echo `date` >> run.log &&

source venv/bin/activate
python3 punch.py

echo 'finish' >> run.log