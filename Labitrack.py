#!/usr/bin/env python
# coding: utf-8

#####################################################
#                                                   #
# Labitrack v 0.1 - (Beerware) - 2010 panton, halfd #
#                                                   #
#####################################################


import Tkinter as T
import barcode.barcode as B
import opencv
#import opencv.adaptors
import ImageTk
from opencv import highgui

import os, sqlite3, random, time

# Application class
os.chdir('/home/panton/Documents/labitrack/')

class Labitrack:
    def __init__(self, master):
	self.conn = sqlite3.connect('objects.db')
	self.cur = self.conn.cursor()

	# Get the next id man
	self.cur.execute('select oid+1 from objects order by oid desc limit 1;')
	self.id_val = self.cur.fetchone()[0]

	self.camera = highgui.cvCreateCameraCapture(0)
	self.image = None

	# Create a label instance
        self.label = B.Label()

        # The master frame
        self.frame = T.Frame(master) 

	# Frame for camera input
	camera_frame = T.Frame(self.frame, relief="sunken", borderwidth=1, pady=20)

	self.imagecanvas = T.Canvas(camera_frame, width=320, height=240)

        # take picture button
        picture_button = T.Button(camera_frame, text="Take picture", anchor=T.W, command=self.takepicture) 

        # Frame for input
        input_frame = T.Frame(self.frame, relief="sunken", borderwidth=1, pady=20)

        # Object name label and input field
        object_name_label = T.Label(
            input_frame, 
            text="Name of item", 
            font=("Helvetica", 17), 
            anchor=T.W, 
            justify=T.LEFT, 
            width=50, 
            padx=20, 
            pady=5
        )

        self.object_name = T.Entry(
            input_frame,
            width=64,
            font=("Helvetica", 14), 
            border=0,
            highlightcolor="#34fe32"
        )

        # Object tagline label and input field
        object_tagline_label = T.Label(
            input_frame, 
            text="Tagline", 
            font=("Helvetica", 17), 
            anchor=T.W, 
            justify=T.LEFT, 
            width=50, 
            padx=20, 
            pady=5
        )
        
        self.object_tagline = T.Entry(
            input_frame,
            width=64,
            font=("Helvetica", 14), 
            border=0,
            highlightcolor="#34fe32"
        )

	# Frame for options
	option_frame = T.Frame(self.frame, relief="sunken", border=1, pady=20, padx=20)

	self.personal = T.IntVar()
	self.choice_personal = T.Checkbutton(option_frame, text="Personal", variable=self.personal)

	self.manual = T.IntVar()
	self.choice_manual = T.Checkbutton(option_frame, text="Manual", variable=self.manual)

	self.dnh = T.IntVar()
	self.choice_dnh = T.Checkbutton(option_frame, text="Do not hack", variable=self.dnh)

        # Frame for buttons
        button_frame = T.Frame(self.frame, relief="sunken", border=1, pady=20, padx=20)

        # Preview button
        preview_button = T.Button(button_frame, text="Preview", anchor=T.W, command=self.create_preview) 

        # Print button
        print_button = T.Button(button_frame, text="Print", anchor=T.E, command=self.create_print) 

	# Pack camera input
	camera_frame.pack(side="left")
	self.imagecanvas.pack(side="top")
	picture_button.pack(side="top")

        # Pack input frame and widgets
        input_frame.pack(side="top",expand="true") 

        object_name_label.pack(side="top")
        self.object_name.pack(side="top", expand="true")
       
        object_tagline_label.pack(side="top")
        self.object_tagline.pack(side="top")

	# Pack choice frame and widgets
	option_frame.pack(side="left",expand="true") 

	self.choice_personal.pack(side="left")
	self.choice_manual.pack(side="left")
	self.choice_dnh.pack(side="left")

        # Pack button frame and widgets
        button_frame.pack(side="left")

        preview_button.pack(side="left")
        print_button.pack(side="left")

        # Set window-title and pack the master frame
        self.frame.master.title('Labitrack')
        self.frame.pack()
	#self.display_picture()

    def create_preview(self):
	self.name_val = self.object_name.get()
	self.tagline_val = self.object_tagline.get()
	self.personal_val = self.personal.get()
	self.manual_val = self.manual.get()
	self.dnh_val = self.dnh.get()

	self.cur.execute('select oid+1 from objects order by oid desc limit 1;')
	self.id_val = self.cur.fetchone()[0]

        self.label.create(
		self.name_val,
		self.tagline_val,
		self.id_val,
		labelpersonal=self.personal_val,
		labelmanual=self.manual_val,
		labeldnh=self.dnh_val
	)

    def create_print(self):
	self.cur.execute('insert into objects (name, tagline) values (?, ?);', (self.name_val, self.tagline_val))
	self.label.printlabel()
	self.conn.commit()

    def display_picture(self):
	imagecapture = highgui.cvQueryFrame(self.camera)
	self.pilimage = opencv.adaptors.Ipl2PIL(imagecapture)
	miniimage = self.pilimage.resize((320,240))
	self.image = ImageTk.PhotoImage(miniimage, master=self.frame)
	self.imagecanvas.create_image(0,0,image=self.image,anchor="nw")
	self.imagecanvas.update()
	time.sleep(0.1)
	self.display_picture()

    def takepicture(self):
	self.pilimage.save('images/%d.png' % (self.id_val, ))

# Create application and run mainloop
top = T.Tk()
labitrack = Labitrack(top)
top.mainloop()
