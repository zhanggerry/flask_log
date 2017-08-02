#-*- coding: utf-8 -*-
#!E:\python\python.exe

from app import app
app.secret_key = 'sth. random as a encrypt key.'
app.run(debug = True)


