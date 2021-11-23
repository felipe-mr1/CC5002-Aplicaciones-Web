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

data = edb.getEventsPerDay()

l = []

def time(date):
    date = str(date)
    date = date.split('-')
    return date

for d in data:
    a = list(d)
    var = time(a[0])
    a[0] = int(var[0])*10000 + int(var[1])*100 + int(var[2])
    #a[0] = time(a[0])
    l.append(a)


#data = dict(data)

print(l)