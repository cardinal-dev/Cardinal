#!/bin/bash

rm /usr/bin/scout
pyinstaller --onefile scout.py
cp dist/scout /usr/bin
rm -r dist build scout.spec
