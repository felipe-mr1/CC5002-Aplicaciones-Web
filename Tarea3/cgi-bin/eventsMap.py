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

data = edb.getMapEvents()

l= []

for d in data:
    a = list(d)
    count = 0
    for b in a:
        if count == 6 or count == 7:
            a[count] = str(a[count])
        if count == 1:
            a[count] = edb.getComuna(a[count])[0][0]
        if count == 0:
            a[count] = edb.getPhoto(a[count])[0][0]
        count+=1
        
    l.append(a)

print(l, file=utf8stdout)
