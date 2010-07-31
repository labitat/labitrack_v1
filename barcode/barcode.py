#!/usr/bin/env python

# coding: utf-8

import sys, pyx, os
import qrcode

from urllib2 import urlopen
from PIL import Image
from random import randint

class Label:
    def __init__(self):
	pyx.text.set(mode="latex")
	pyx.text.preamble(r"\parindent=0pt")
	self.e = qrcode.Encoder()

    def create(self, labelname, labelinfo, labelid, labelpersonal=False, labelmanual=False, labeldnh=True):
        labelid = int(labelid)
	self.printedid = labelid

        width = 5.5
	image = self.e.encode('http://o.labitat.dk/%d' % labelid, version=2, eclevel=self.e.eclevel.L)

	c = pyx.canvas.canvas()
	c.insert(pyx.bitmap.bitmap(0, 0.4, image, height=2.5))
	c.text(2.7, 2.9, r"{\textbf{\Large\sffamily %s}}" % labelname , [pyx.text.halign.boxleft, pyx.text.valign.top])
	c.text(2.7, 2.35, r"{\sffamily ID: %d}" % labelid , [pyx.text.halign.boxleft, pyx.text.valign.top])

	c.text(2.7, 1.96, r"{\textit{\sffamily %s}}" % labelinfo , [pyx.text.parbox(width), pyx.text.halign.boxleft, pyx.text.valign.top])

	if labelpersonal:
	    im = Image.open("/home/halfd/labitrack/barcode/person.jpg")
	    c.insert(pyx.bitmap.bitmap(2.7,0.1+0.4,im,height=0.7))

	if labelmanual:
	    im = Image.open("/home/halfd/labitrack/barcode/manual.jpg")
	    c.insert(pyx.bitmap.bitmap(3.6,0.1+0.4,im,height=0.7))

	if labeldnh:
	    tbox = pyx.text.text(2.5+width, 0.31+0.4,  r"{\textbf{\Large\sffamily DNH}}", [pyx.text.halign.boxright, pyx.text.valign.bottom])
	    tpath = tbox.bbox().enlarged(3*pyx.unit.x_pt).path()
	    c.draw(tpath, [pyx.deco.stroked()])
	    c.stroke(tpath, [pyx.style.linewidth.Thick])
	    c.insert(tbox)

	sc = pyx.canvas.canvas()
	sc.insert(c, [pyx.trafo.rotate(90)])

	sc.writePDFfile("print")
	os.system("pdftops print.pdf")
	os.system("evince print.ps")

    def printlabel(self):
	os.system("lpr -PQL-570 print.ps")
	os.system("mv print.ps printed/%s.ps" % (self.printedid, ) )
	os.system("rm print.pdf")
