# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

fname=input('Enter File Name')
try:
    fhand=open(fname)
except:
    print('File cannot be opened:', fname)
count =0
for line in fhand:
    newline=line.upper()
    print(newline)