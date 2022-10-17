from tkinter import *
from random import randint
from playsound import playsound
from multiprocessing import Process
from PIL import Image, ImageTk
from time import sleep
from tkinter import messagebox
from pathlib import Path

# river link = 'https://www.youtube.com/watch?v=C3rZPuyydKg&ab_channel=SFX'
# bamboo link = 'https://www.youtube.com/watch?v=v7-PjPp1JKw&ab_channel=SoundEffect'

PATH = Path(__file__).parent.absolute()

bamboo = f'{PATH}/bamboo.mp3'
river = f'{PATH}/river.mp3'

x = 10
y = 60

def update():
    global x, y
    x = int(minimum.get())
    minimum.delete(0, END)
    y = int(maximum.get())
    maximum.delete(0, END)

go = False
f = False

def stop_hit():
    drum.itemconfig(taiko_drum, image=taiko_img)

def play():
    global go
    if go:
        global d
        drum.itemconfig(taiko_drum, image=taiko_hit)
        d = Process(target=playsound, args=(bamboo,))
        drum.after(100, d.start)
        drum.after(100, stop_hit)
        iai()

def iai():
    global x, y
    window.after(randint(x * 1000, y * 1000), play)

window = Tk()
window.title('Iai')
window.config(padx=20, pady=50)

iai_label = Label(text='Drum Switch')
iai_label.grid(row=0, column=0)

river_label = Label(text='Bg Switch')
river_label.grid(row=0, column=2)

with Image.open(f'{PATH}/on.png') as im:
    (width, height) = (im.width // 2, im.height // 2)
    new_on = im.resize((width,height))

with Image.open(f'{PATH}/off.png') as im:
    (width, height) = (im.width // 2, im.height // 2)
    new_off = im.resize((width,height))

with Image.open(f'{PATH}/taiko.png') as im:
    (width, height) = (round(im.width * 1.05), round(im.height * 1.05))
    taiko_hit_img = im.resize((width,height))


on_img = ImageTk.PhotoImage(new_on)
off_img = ImageTk.PhotoImage(new_off)
taiko_img = PhotoImage(file=f'{PATH}/taiko.png')
taiko_hit = ImageTk.PhotoImage(taiko_hit_img)

def iai_switch():
    global go

    if go:
        iai_button.config(image=off_img)
        go = False
    
    else:
        iai_button.config(image=on_img)
        go = True
        iai()

iai_button = Button(image=off_img, command=iai_switch)
iai_button.grid(row=1, column=0)

def dummy():
    pass

p = Process(target=dummy, args=())
p.start()
p.terminate()
d = Process(target=dummy, args=())
d.start()
d.terminate()

def refresh():
    if p.is_alive():
        river_switch()
        sleep(1)
        river_switch()

p = Process(target=dummy, args=())
p.start()
p.terminate()

def river_switch():
    global p, f

    if  f:
        river_button.config(image=off_img)
        p.terminate()
        f = False

    else:
        river_button.config(image=on_img)
        p = Process(target=playsound, args=(river,))
        p.start()
        f = True
        window.after(305000, refresh)

def on_closing():
    if messagebox.askokcancel('Exit', 'Do you want to exit application?'):
        global p, d
        if p.is_alive():
            p.terminate()
        if d.is_alive():
            d.terminate()
        window.destroy()

river_button = Button(image=off_img, command=river_switch)
river_button.grid(row=1, column=2)

drum = Canvas(width=600, height=600)
taiko_drum = drum.create_image(300, 300, image=taiko_img)

drum.grid(row=1, column=1)

change_time = Label(text = 'If you want to change minimum and maximum seconds for delay, enter below, default is between 10 and 60 seconds.\nEnter minimum value on left and maximum on right and press update button to apply.')

change_time.grid(row=2, column=0, columnspan=3, pady=30)

minimum = Entry()
minimum.grid(row=3, column=0)

maximum= Entry()
maximum.grid(row=3, column=1)

new_values = Button(text='update', command=update)
new_values.grid(row=3, column=2)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
