from django.db import models
from django.db.models.signals import post_save
from AwazApp.models import *
import string
f = open("output.txt",'r')
lines = f.readlines()
'''for x in lines:'''
i = 1
while i:
	x = lines[55]
	for k, v in x.iteritems():
		print k, v
	x = ''.join([ c for c in x if c not in ("}", "{")])
	#print x
	y = x.split(",")
	z =  "".join(y)
	y[0] = ' '+y[0]
	l = []
	for el in y:
		el = el.lstrip(' ')
		el = el.lstrip('u')
		els = el.split(":")
		for e in els:
			if e[0] == 'u':
				e = e.lstrip('u')
			e = e.lstrip(' ')
		
			if e[0] == 'u':
				e = e.lstrip('u')
		
			l.append(e)
	l1 = []	
	l2 = []	
	for i in  range(len(l)):
		if i%2 == 0:
			l1.append(l[i])
		else:
			l2.append(l[i])
	#for el in l2:
	#	print el
	i = 0
	 
'''
	d = Dictionary()
	d.tmp =l2[0]
	d.lang = l2[1]
	d.uid = l2[2]
	d.name =l2[3]
	d.FRA =l2[4]
	d.EN =l2[5]
	d.PARENT =l2[6] 
	d.IMG =l2[7]
	d.CID = l2[8]
	d.MOR =l2[9]
	d.SP = l2[10]
	d.LST = l2[11]
	d.ANI = l2[12]
	d.POS = l2[13]
	d.SC = l2[14]
	d.AS = l2[15]
	d.NUM = l2[16]
	d.ABT = l2[17]
	d.PAR = l2[18]
	d.LEX = l2[19]
	d.SEM = l2[20]
	d.AUDIO = l2[21]
	d.save()'''


	


