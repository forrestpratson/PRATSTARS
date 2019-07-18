from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

def filef():
    master.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",)
    fnamee.delete(0, END)
    fnamee.insert(END, master.filename)

def savef():
    master.filename =  filedialog.askdirectory(initialdir = "/",title = "Select file",)
    savee.delete(0, END)
    savee.insert(END, master.filename)

master = Tk()

labelfont = ('helvetica', 30, 'bold')
borderz = Label(master, text=' ')
borderz.config(font=labelfont)
borderz.grid(row=6,column=1)

borderx = Label(master, text='    ')
borderx.config(font=labelfont)
borderx.grid(row=0,column=0)

borderx = Label(master, text='    ')
borderx.config(font=labelfont)
borderx.grid(row=0,column=4)

border = Label(master, text=' ')
border.config(font=labelfont)
border.grid(row=10,column=1)

border = Label(master, text=' ')
border.config(font=labelfont)
border.grid(row=8,column=1)

title = Label(master, text='PRATSTARS')
title.config(font=labelfont)
title.grid(row = 0,column=1,columnspan = 2)

logo = Image.open("/Users/forrestpratson/CERN_PACKAGE/PRATSTAR/GUI/Logo.png")
logo = logo.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
img = ImageTk.PhotoImage(logo)
panel = Label(master, image = img)
panel.grid(row=1,column=1,columnspan=2)

ename_l = Label(master, text='Event Number:')
ename_l.grid(row=5,column=1,sticky=E)
ename = Entry(master)
ename.grid(row=5,column=2)
ename.focus_set()

save=Button(master, text="Save Folder:", width=15, command=savef)
save.grid(row=4,column=1,sticky=E)
savee=Entry(master)
savee.grid(row=4,column=2)

threshe=Entry(master)
threshe.grid(row=6,column=2)
thresh=Label(master, text='*Momentum Threshold (MeV):')
thresh.grid(row=6,column=1)

fnamel = Button(master, text="File:", width=15, command=filef)
fnamel.grid(row=3,column=1,sticky=E)
fnamee = Entry(master)
fnamee.grid(row=3,column=2)

view_l = Frame(master)
view_l.grid(row=7,column=1)
view_l.columnconfigure(0, weight = 1)
view_l.rowconfigure(0, weight = 1)

views = StringVar(master)
choices = { 'Transverse','Longitudinal','Both'}
views.set('Transverse')
popupMenu = OptionMenu(view_l, views, *choices)
Label(view_l, text="*Choose a View").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)


pwd = os.getcwd()

def Go():
    evt_num = ename.get()
    save_loc = savee.get()
    
    if save_loc=='':
        save_loc=pwd
    if switch_variable.get() == 'daod':
        command = "pratstar_DAOD.py"
        if str(switch_variable.get()) == 'daod' and str(fnamee.get())[-4:]== '.lhe':
            error = Toplevel()
            message = Label(error, text='ERROR: WRONG FILE TYPE')
            message.pack()
        os.system("python " + command + " --view=" +views.get()+ " --show=True --output=" + save_loc + " --event=" + str(evt_num) + " --file=" + str(fnamee.get()) + " --labels=" + str(var1.get()) + " --thresh=" + str(threshe.get()))
    if switch_variable.get() == 'lhe':
        command = "pratstar_LHE.py"
        os.system("python " + command + " --output=" + save_loc + " --event=" + str(evt_num) + " --file=" + str(fnamee.get()))

b = Button(master, text="Go!", width=15,height=2, command=Go)
b.grid(row=9,column=1,columnspan=2)
warnfont = ('helvetica', 10, 'italic')
warn = Label(master, text='*For DAOD Visualization Only')
warn.config(font=warnfont)
warn.grid(row=8,column=1,columnspan=2)

var1 = IntVar()
Checkbutton(master, text="*Labels", variable=var1).grid(row=7, column=2,sticky=W)
status = False


switch_frame = Frame(master)
switch_frame.grid(row=2,column=1,columnspan=2)

switch_variable = StringVar(value="off")
lhe_button = Radiobutton(switch_frame, text="DAOD Visualization", variable=switch_variable,
                            indicatoron=False, value="daod", width=18)
daod_button = Radiobutton(switch_frame, text="LHE Visualization", variable=switch_variable,
                            indicatoron=False, value="lhe", width=18)

lhe_button.pack(side="left")
daod_button.pack(side="left")

mainloop()

