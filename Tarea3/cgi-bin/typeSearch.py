#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb

cgitb.enable()
from eventDB import Event

print('Content-type: text/html; charset=UTF-8')
print('')
#print('Content-type: text/html\r\n\r\n')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

form = cgi.FieldStorage()
edb = Event('localhost', 'root', '', 'tarea2')

data = edb.getTypeEvents()

l = []

for d in data:
    a = list(d)
    l.append(a)

print(l, file=utf8stdout)