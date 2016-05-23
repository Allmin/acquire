# -*- coding: utf-8 -*-
"""
author: Allmin Pradhap Singh Susaiyah (allmin123@gmail.com)
description: to acquire images for learning a cascade classifier
"""
import Tkinter
from PIL import ImageTk
import cv2
import time
import numpy as np
from scipy.misc import toimage
import pickle
import os.path

def closex():
    global ind
    with open('ind.pickle', 'w') as f:
        pickle.dump(ind, f)
    root.destroy()
    if cv2.VideoCapture(0).isOpened():
        cam.release()
           
def close(event):
    closex()

def frame_rate():       
    global fps_f, fps_t, frame_rt 
    now = int(time.time())    
    fps_f += 1
    if fps_t == 0:
        fps_t = now
    elif fps_t < now:
        frame_rt = np.uint8(1.0 * fps_f / (now-fps_t))
        screen_op = str(frame_rt) + ' FPS'
        fr_display.config(text = screen_op)
        fps_t = now
        fps_f = 0

class callbacks:
    def __init__(self):  
        self.helm_top_left =[ 0, 0]
        self.helm_bot_right=[40,40]
        self.capture_image_stat=0
    def start_rect(self,event):
        self.helm_top_left = [event.x, event.y]     
    def drag_rect(self,event1):
        self.helm_bot_right = [event1.x, event1.y]     
    def stop_rect(self,event2):
        self.helm_bot_right = [event2.x, event2.y]
    def capture_image(self):
        self.capture_image_stat=1


def show_frame(first=False):
    global ind
    if first: 
        root.geometry('%dx%d' % (660,660))
    (a,i)=cam.read()
    i_rgb=cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
#    gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    frame_rate()
    
    if gui.capture_image_stat==1:   
        ind=ind+1
        ind_display.config(text = str(ind))
        cropped_gray=i_rgb[gui.helm_top_left[1]:gui.helm_bot_right[1],gui.helm_top_left[0]:gui.helm_bot_right[0],:]        
        pil_save_img=toimage(cropped_gray)
        fname= 'img'+ str(ind) + '.jpg'
        pil_save_img.save(fname)
        gui.capture_image_stat=0
        
    cv2.rectangle(i_rgb,(gui.helm_top_left[0],gui.helm_top_left[1]),(gui.helm_bot_right[0],gui.helm_bot_right[1]),(255,0,0),3)
    pil_disp_img=toimage(i_rgb)
    tkpi = ImageTk.PhotoImage(pil_disp_img)
    label_image.imgtk = tkpi
    label_image.configure(image = tkpi)
    label_image.after(1, show_frame)

ind = 0
if os.path.isfile('ind.pickle'):
    with open('ind.pickle') as f:
        ind = pickle.load(f)       
fps_f = 0
fps_t=0
frame_rt=0
cam=cv2.VideoCapture(0)
gui = callbacks()   
root = Tkinter.Tk()
root.title('Seek Thermal camera')   
root.bind('<Escape>', close)
root.protocol('WM_DELETE_WINDOW', closex) 
label_image = Tkinter.Label(root)
fr_display = Tkinter.Label(root)
ind_display = Tkinter.Label(root)
b_capture_image = Tkinter.Button(root, text="Capture Image", command=gui.capture_image)
label_image.grid(row = 0, column = 0,columnspan=5)
fr_display.grid(row = 1, column = 4)
b_capture_image.grid(row = 1, column = 0)
ind_display.grid(row = 1, column = 1)
ind_display.config(text = str(ind))
label_image.bind("<Button-1>",gui.start_rect)
label_image.bind("<B1-Motion>",gui.drag_rect)
label_image.bind("<ButtonRelease-1>",gui.stop_rect)
show_frame(first=True)
root.mainloop()
